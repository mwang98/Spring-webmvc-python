package com.yuntao.hello;

import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

/**
 * Created by pengyuntao on 16/10/12.
 */
@Controller
@RequestMapping(value = "/", method = RequestMethod.GET)
public class HelloController {

    @RequestMapping(value = "/welcome", method = RequestMethod.GET)
    public String printHello(ModelMap model) {
        System.out.println("In HelloController");
        model.addAttribute("msg", "Spring MVC Hello World");
        model.addAttribute("name", "yuntao");
        return "hello";
    }
}
