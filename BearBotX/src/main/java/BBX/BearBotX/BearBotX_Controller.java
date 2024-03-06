package BBX.BearBotX;

import com.fasterxml.jackson.databind.JsonDeserializer;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.io.Console;
import java.io.IOException;

@RestController
@CrossOrigin(origins = "http://localhost:4200")
class BearBotX_Controller {

    Client client=new Client();
    JSON_Manager json_manager=new JSON_Manager();

    private String text="Fabi der G";

    @GetMapping("/test")
    String getString(){
        return text;
    }


    @PostMapping("/connect")
    public String connect(@RequestBody String ip){
        String test;
        try{
            System.out.println(ip);
            test=client.connect(ip);
        }catch(Exception ex){
            return "Exception:\n"+ ex.getMessage();
        }
        return test;
    }

    @GetMapping("/sensordata")
    public String getData(){
        //return client.getData();
        return "example Data 1\nexample Data 2";
    }

    @PostMapping("/velocity")
    public void setVelocity(@RequestBody String speed){
        //client.send("{\"speed\":"+speed);
        System.out.println(speed);
    }

    @GetMapping("/disconnect")
    public String disconnect(){
        String answer="Disconnection was unsuccessful";
        try
        {
            answer=client.closeConnection();
        }catch(Exception ex){
            answer= "Disconnect was unsuccessful\nException: "+ex.getMessage();
        }
        return answer;
    }

    @PostMapping("/direction")
    public void listen(@RequestBody String dir){
        System.out.println(dir);
        String[] dirArray=json_manager.toStringArray(dir);
        System.out.println(dirArray[0]+" "+dirArray[1]);
    }
}
