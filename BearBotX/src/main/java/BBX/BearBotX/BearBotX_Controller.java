package BBX.BearBotX;

import com.fasterxml.jackson.databind.JsonDeserializer;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
class BearBotX_Controller {

    Client client=new Client();

    private String text="Seavas";

    @GetMapping("/test")
    String getString(){
        return text;
    }


    @PostMapping("/connect")
    public String connectToServer(@RequestBody String ip){
        String test;
        try{
            System.out.println(ip);
            test=client.connect(ip);
        }catch(Exception ex){
            return "Exception:\n"+ ex.getMessage();
        }
        return test;
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
