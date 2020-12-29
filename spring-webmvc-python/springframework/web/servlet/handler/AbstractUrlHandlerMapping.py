import logging

from sprngframework.web.servlet.handler import AbstractHandlerMapping, MatchableHandlerMapping, RequestMatchResult
from springframework.utils.mock.inst import RequestPath, HttpServletRequest, ServletRequestPathUtils
# TODOHandlerExecutionChain, HandlerInterceptor
from springframework.web.servlet import HandlerExecutionChain, HandlerInterceptor
from springframework.web.util import UrlPathHelper


class AbstractUrlHandlerMapping(AbstractHandlerMapping, MatchableHandlerMapping):

    rootHandler: object = None
    _useTrailingSlashMatch: bool = False
    lazyInitHandlers: bool = False
    handlerMap = dict()
    pathPatternHandlerMap: dict()

    def setRootHandler(self, rootHandler: object) -> None:
        self.rootHandler = rootHandler

    def getRootHandler(self) -> object:
        return self.rootHandler

    def setUseTrailingSlashMatch(self, useTrailingSlashMatch: bool):
        self._useTrailingSlashMatch = useTrailingSlashMatch
        if self.getPatternParser() is not None:
            self.getPatternParser().setMatchOptionalTrailingSeparator(useTrailingSlashMatch)

    def useTrailingSlashMatch(self):
        return self._useTrailingSlashMatch

    def setLazyInitHandlers(self, lazyInitHandlers: bool):
        self.lazyInitHandlers = lazyInitHandlers

    def getHandlerInternal(self, request: HttpServletRequest) -> object:
        lookupPath: str = self.initLookupPath(request)
        handler: object = None
        if self.usesPathPatterns():
            path: RequestPath = ServletRequestPathUtils.getParsedRequestPath(request)
            handler = self.lookupHandler(path, lookupPath, request)
        else:
            handler = self.lookupHandler(lookupPath, request)

        if handler is None:
            rawHandler: object = None
            if lookupPath == '/':
                rawHandler = self.getRootHandler()
            if rawHandler is None:
                rawHandler = self.getDefaultHandler()
            else:
                if isinstance(rawHandler, str):
                    handlerName = str(rawHandler)
                    rawHandler = self.obtainApplicationContext().getBean(handlerName)
                self.validateHandler(rawHandler, request)
                handler = self.buildPathExposingHandler(rawHandler, lookupPath, lookupPath, None)
        return handler

    def lookupHandler(self, arg1, arg2, arg3=None) -> object:
        if isinstance(arg1, object) and isinstance(arg2, str):

            path = arg1
            lookupPath = arg2
            request = arg3

            handler: object = self.getDirectMatch(lookupPath, request)
            if handler is not None:
                return handler

            matches = list()
            for pattern in self.pathPatternHandlerMap.keys():
                if pattern.matches(path):
                    matches.append(pattern)

            if not matches:
                return None
            else:
                # TODO
                # matches.sort(PathPattern.SPECIFICITY_COMPARATOR)
                logging.debug(f"Matching patterns: {matches}")

            pattern = matches[0]
            handler = self.pathPatternHandlerMap.get(pattern)
            if isinstance(handler, str):
                handlerName = handler
                handler = self.obtainApplicationContext().getBean(handlerName)

            self.validateHandler(handler, request)
            pathWithinMapping = pattern.extractPathWithinPattern(path)
            return self.buildPathExposingHandler(handler, pattern.getPatternString(), pathWithinMapping.value(), None)

        elif isinstance(arg1, str) and isinstance(arg2, object):

            lookupPath = arg1
            request = arg2

            handler = self.getDirectMatch(lookupPath, request)
            if handler is None:
                return handler

            matchingPatterns = list()
            for registeredPattern in self.handlerMap.key():
                if self.getPathMatcher().match(registeredPattern, lookupPath):
                    matchingPatterns.append(registeredPattern)
                elif self.useTrailingSlashMatch():
                    if (not registeredPattern.endsWith("/")) and self.getPathMatcher().match(registeredPattern + "/", lookupPath):
                        matchingPatterns.add(registeredPattern + "/")

            bestMatch: str = None
            patternComparator = self.getPathMatcher().getPatternComparator(lookupPath)

            if matchingPatterns:
                # TODO
                # matchingPatterns.sort(patternComparator)
                logging.info(f"Matching patterns: {matchingPatterns}")
                bestMatch = matchingPatterns[0]

            if bestMatch is not None:
                handler = self.handlerMap.get(bestMatch)
                if handler is None:
                    if bestMatch.endsWith("/"):
                        handler = self.handlerMap.get(bestMatch[:-1])
                    if handler is None:
                        raise Exception(f"Could not find handler for best pattern match [{bestMatch}]")

                # Bean name or resolved handler?
                if isinstance(handler, str):
                    handlerName: str = handler
                    handler = self.obtainApplicationContext().getBean(handlerName)

                self.validateHandler(handler, request)
                pathWithinMapping = self.getPathMatcher().extractPathWithinPattern(bestMatch, lookupPath)

                # There might be multiple 'best patterns', let's make sure we have the correct URI template variables
                # for all of them
                uriTemplateVariables = dict()
                for matchingPattern in matchingPatterns:
                    if patternComparator.compare(bestMatch, matchingPattern) == 0:
                        var: dict = self.getPathMatcher().extractUriTemplateVariables(matchingPattern, lookupPath)
                        decodedVars: dict = self.getUrlPathHelper().decodePathVariables(request, var)
                        uriTemplateVariables.update(decodedVars)

                if uriTemplateVariables:
                    logging.info(f"URI variables {uriTemplateVariables}")

                return self.buildPathExposingHandler(handler, bestMatch, pathWithinMapping, uriTemplateVariables)

            # No handler found...
            return None

    def getDirectMatch(self, urlPath: str, request: HttpServletRequest) -> object:
        handler = self.handlerMap.get(urlPath)
        if handler is not None:
            # Bean name or resolved handler?
            if isinstance(handler, str):
                handlerName: str = handler
                handler = self.obtainApplicationContext().getBean(handlerName)
            self.validateHandler(handler, request)
            return self.buildPathExposingHandler(handler, urlPath, urlPath, None)
        return None

    def validateHandler(self, handler: object, request) -> None:
        pass

    def buildPathExposingHandler(
        self,
        rawHandler: object,
        bestMatchingPattern: str,
        pathWithinMapping: str,
        uriTemplateVariables: dict
    ) -> object:
        chain = HandlerExecutionChain(rawHandler)
        chain.addInterceptor(PathExposingHandlerInterceptor(bestMatchingPattern, pathWithinMapping))
        if not uriTemplateVariables:
            chain.addInterceptor(UriTemplateVariablesHandlerInterceptor(uriTemplateVariables))
        return chain

    def exposePathWithinMapping(self, bestMatchingPattern: str, pathWithinMapping: str, request) -> None:
        request.setAttribute(self.BEST_MATCHING_PATTERN_ATTRIBUTE, bestMatchingPattern)
        request.setAttribute(self.PATH_WITHIN_HANDLER_MAPPING_ATTRIBUTE, pathWithinMapping)

    def exposeUriTemplateVariables(self, uriTemplateVariables: dict, request) -> None:
        request.setAttribute(self.URI_TEMPLATE_VARIABLES_ATTRIBUTE, uriTemplateVariables)

    def match(self, request, pattern: str):
        assert self.getPatternParser() is not None, "This HandlerMapping uses PathPatterns."
        lookupPath: str = UrlPathHelper.getResolvedLookupPath(request)
        if (self.getPathMatcher().match(pattern, lookupPath)):
            return RequestMatchResult(pattern, lookupPath, self.getPathMatcher())
        elif self.useTrailingSlashMatch():
            if not pattern.endsWith("/") and self.getPathMatcher().match(pattern + "/", lookupPath):
                return RequestMatchResult(pattern + "/", lookupPath, self.getPathMatcher())
        return None

    def registerHandler(self, urlPaths: list, beanName: str):
        assert urlPaths, "URL path array must not be null"
        if isinstance(urlPaths, list):
            for urlPath in urlPaths:
                self.registerHandler(urlPath, beanName)
        else:
            urlPath = urlPaths
            handler = beanName
            assert urlPath, "URL path must not be null"
            assert handler, "Handler object must not be null"
            resolvedHandler = handler

            # Eagerly resolve handler if referencing singleton via name.
            if not self.lazyInitHandlers and isinstance(handler, str):
                handlerName: str = handler
                applicationContext = self.obtainApplicationContext()
                if applicationContext.isSingleton(handlerName):
                    resolvedHandler = applicationContext.getBean(handlerName)

            mappedHandler = self.handlerMap.get(urlPath)
            if mappedHandler is nt None:
                if mappedHandler != resolvedHandler:
                    raise Exception(f"""
                        Cannot map {self.getHandlerDescription(handler)} to URL path [{urlPath}
                        ]: There is already {self.getHandlerDescription(mappedHandler)} mapped."
                    """)
            else:
                if urlPath == "/":
                    logging.info(f"Root mapping to {getHandlerDescription(handler)}")
                elif urlPath == "/*":
                    logging.info(f"Default mapping to {getHandlerDescription(handler)}")
                    self.setDefaultHandler(resolvedHandler)
                else:
                    self.handlerMap[urlPath] = resolvedHandler
                    if self.getPatternParser() is not None:
                        self.pathPatternHandlerMap[self.getPatternParser().parse(urlPath)] = resolvedHandler
                    logger.info(f"Mapped [{urlPath}] onto {self.getHandlerDescription(handler)}")

    def getHandlerDescription(self, handler: object) -> str:
        return f"'handler'" if isinstance(handler, str) else str(handler)

    def getHandlerMap(self) -> dict:
        return self.handlerMap.copy()

    def getPathPatternHandlerMap(self) -> dict:
        return self.pathPatternHandlerMap.copy()

    def supportsTypeLevelMappings(self) -> bool:
        return False


class PathExposingHandlerInterceptor(HandlerInterceptor):

    def __init__(self, bestMatchingPattern: str, pathWithinMapping: str):
        self.bestMatchingPattern: str = bestMatchingPattern
        self.pathWithinMapping: str = pathWithinMapping

    def preHandle(self, request, response, handler):
        self.exposePathWithinMapping(self.bestMatchingPattern, self.pathWithinMapping, request)
        # TODO: BEST_MATCHING_HANDLER_ATTRIBUTE, INTROSPECT_TYPE_LEVEL_MAPPING
        # dont know where it is from
        request.setAttribute(self.BEST_MATCHING_HANDLER_ATTRIBUTE, handler)
        request.setAttribute(self.INTROSPECT_TYPE_LEVEL_MAPPING, supportsTypeLevelMappings())
        return True


class UriTemplateVariablesHandlerInterceptor(HandlerInterceptor):

    def __init__(self, uriTemplateVariables: dict):
        self.uriTemplateVariables = uriTemplateVariables

    def preHandle(self, request, response, handler):
        self.exposeUriTemplateVariables(this.uriTemplateVariables, request);
        return True
