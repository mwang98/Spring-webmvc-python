package com.yuntao.hello;

import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.Controller;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.web.servlet.mvc.AbstractController;
import java.time.LocalDateTime;

public class HelloController2 implements Controller{

    @Override
    public ModelAndView handleRequest(HttpServletRequest request, HttpServletResponse response) throws Exception {
        System.out.println("In HelloController2");
        ModelAndView mav = new ModelAndView();
        // String name = request.getParameter("name");
        // mav.addObject("message", "team4");
        // mav.addObject("now", LocalDateTime.now().toString());
        mav.addObject("msg", "Hello Spring mvc");
        mav.addObject("name", "mike");
        mav.setViewName("hello");

        // return the name of the file to be loaded "hello_world.jsp"
        return mav;
    }
}
