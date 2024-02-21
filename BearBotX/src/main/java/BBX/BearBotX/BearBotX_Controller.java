package BBX.BearBotX;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
class BearBotX_Controller {

    Client client=null;
    private int i=8;

    @GetMapping("/test")
    int getInt(){
        return i;
    }


    @PostMapping("/connect")
    public String connectToServer(@RequestBody String ip){
        try{
            client=new Client(ip);
        }catch(Exception ex){
            return ex.getMessage();
        }
        return "Connection Successful";
    }

    @PostMapping("/send")
    public void send(@RequestBody String command){
        client.send(command);
    }

    @GetMapping("/data")
    public String getData(){
        return client.getData();
    }

    @PostMapping("/velocity")
    public void setVelocity(@RequestBody int speed){
        client.setSpeed(speed);
    }
}
