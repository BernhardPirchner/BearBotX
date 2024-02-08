package BBX.BearBotX;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
class BearBotX_Controller {

    private int i=8;

    @GetMapping("/test")
    int GetInt(){
        return i;
    }



}
