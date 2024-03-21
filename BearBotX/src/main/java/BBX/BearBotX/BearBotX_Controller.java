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
    MBotListener mbotListener;
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
        //System.out.println(dir);
        //System.out.println(dirArray[1]);
        String command="";

        if(dirArray[1].equals("FWLT")||dirArray[1].equals("FWRT")||dirArray[1].equals("BWLT")||dirArray[1].equals("BWRT")){
             command="MOVE:"+dirArray[1]+":"+speed+",45,RS";
        }else{
             command="MOVE:"+dirArray[1]+":"+speed+",000,RS";
        }
        System.out.println(command);
        //mBot.send(command);
    }

    @GetMapping("/mbot_selection")
    public ArrayList<String> mbotSelection(){
        return mbotListener.getList();
    }

    @PostMapping("/color")
    public void ledColor(@RequestBody String colors){
        System.out.println(colors);

        String[] dirLedColor= json_manager.toStringArray(colors);
        char[] hex=dirLedColor[1].toCharArray();
        String command="MISC:LEDS:"+String.valueOf(hex[1]).toUpperCase()+String.valueOf(hex[2]).toUpperCase()+","+String.valueOf(hex[3]).toUpperCase()+String.valueOf(hex[4]).toUpperCase()+","+String.valueOf(hex[5]).toUpperCase()+String.valueOf(hex[6]).toUpperCase()+","+dirLedColor[3];
        System.out.println(command);
        mBot.send(command);
    }
}