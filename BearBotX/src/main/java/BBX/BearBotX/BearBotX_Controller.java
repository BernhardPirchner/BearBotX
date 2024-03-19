package BBX.BearBotX;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.core.task.SimpleAsyncTaskExecutor;
import org.springframework.core.task.TaskExecutor;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;

@RestController
@CrossOrigin(origins = "http://localhost:4200")
class BearBotX_Controller {
    MBotListener mbotListener=null;
    @Bean
    public CommandLineRunner runner(TaskExecutor taskExecutor){
        return new CommandLineRunner() {
            @Override
            public void run(String... args) throws Exception {
                taskExecutor.execute(mbotListener=new MBotListener());
            }
        };
    }
    MBot mBot =new MBot();
    JSON_Manager json_manager=new JSON_Manager();

    private String text="Fabi L";

    private int speed=0;

    @GetMapping("/test")
    String getString(){
        return text;
    }

    @PostMapping("/connect")
    public String connect(@RequestBody String ip){
        String test;
        try{
            System.out.println(ip);
            test= mBot.connect(ip);
        }catch(Exception ex){
            return "Exception:\n"+ ex.getMessage();
        }
        return test;
    }

    @GetMapping("/sensor_data")
    public String getData(){
        //return client.getData();
        return "example Data 1\nexample Data 2";
    } 

    @PostMapping("/velocity")
    public void setVelocity(@RequestBody String speed){
        String[] temp=json_manager.toStringArray(speed);
        this.speed=Integer.parseInt(temp[temp.length-1]);
        System.out.println(this.speed);
    }

    @GetMapping("/disconnect")
    public String disconnect(){
        String answer="Disconnection was unsuccessful";
        try
        {
            answer= mBot.closeConnection();
        }catch(Exception ex){
            answer= "Disconnect was unsuccessful\nException: "+ex.getMessage();
        }
        return answer;
    }

    @PostMapping("/move")
    public void listen(@RequestBody String dir){
        String[] dirArray=json_manager.toStringArray(dir);
        System.out.println(dir);
        String command="MOVE:FWST:"+speed+",000,RS";
        System.out.println(command);
        //mBot.send(command);
    }

    @GetMapping("/mbot_selection")
    public ArrayList<String> mbotSelection(){
        ArrayList<String> list=new ArrayList<>();
        list.add("Device 1, 0.0.0.1");
        list.add("Device 2, 0.0.0.2");
        list.add("Device 3, 0.0.0.3");

        return list;
    }

    @PostMapping("/color")
    public void ledColor(@RequestBody String colors){
        System.out.println(colors);
    }
}