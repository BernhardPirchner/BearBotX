package BBX.BearBotX;

import jdk.incubator.vector.DoubleVector;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.core.task.SimpleAsyncTaskExecutor;
import org.springframework.core.task.TaskExecutor;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@CrossOrigin(origins = "http://localhost:4200")
class BearBotX_Controller {
    @Bean
    public CommandLineRunner runner(TaskExecutor taskExecutor){
        return new CommandLineRunner() {
            @Override
            public void run(String... args) throws Exception {
                taskExecutor.execute(new MBotListener());
            }
        };
    }
    MBot mBot =new MBot();
    JSON_Manager json_manager=new JSON_Manager();

    private boolean[] light_sensors={false, false, false, false};

    private String text="Fabi L";

    private int speed=0;

    @GetMapping("/test")
    String getString(){
        return text;
    }

    @PostMapping("/connect")
    public String connect(@RequestBody String ip){
        String test="";
        try{
            System.out.println(ip);
            String[] ipArray=json_manager.toStringArray(ip);
            test= mBot.connect(ipArray[1]);
        }catch(Exception ex){
            return "Exception:\n"+ ex.getMessage();
        }
        return test;
    }

    @GetMapping("/sensor_data")
    public ArrayList<String> getData(){
        String json= mBot.getData(";DATA:0:0");
        String[] temp=json_manager.toStringArray(json);
        ArrayList<String> data=new ArrayList<>();
        for (int i=0; (i+1)<=temp.length ; i+=2){
            data.add(temp[i]+": "+temp[i+1]);
            switch (temp[i]){
                case "L2": light_sensors[0]= (Integer.parseInt(temp[i+1])==1); break;
                case "L1": light_sensors[1]= (Integer.parseInt(temp[i+1])==1); break;
                case "R1": light_sensors[2]= (Integer.parseInt(temp[i+1])==1); break;
                case "R2": light_sensors[3]= (Integer.parseInt(temp[i+1])==1); break;
                default: break;
            }
        }
        return data;
    }

    @GetMapping("/light_sensor")
    public boolean[] lightSensor() {
        return light_sensors;
    }


    @PostMapping("/velocity")
    public void setVelocity(@RequestBody String speed){
        String[] temp=json_manager.toStringArray(speed);
        this.speed=Integer.parseInt(temp[temp.length-1]);
        System.out.println(this.speed);
    }

    @GetMapping("/disconnect")
    public String disconnect(){
        String test="";
        try{
            mBot.send(";DISC:0:0");
            test= mBot.disconnect();
        }catch(Exception ex){
            return "Exception:\n"+ ex.getMessage();
        }
        return test;
    }

    @GetMapping("/safety")
    public String safety(){
        String test="";
        try{
            mBot.send(";MISC:SAFE:0");
            test= "worked";
        }catch(Exception ex){
            return "Exception:\n"+ ex.getMessage();
        }
        return test;
    }

    @GetMapping("/autopilot")
    public String autopilot(){
        String test="";
        try{
            mBot.send(";MISC:AUTO:0");
            test= "worked";
        }catch(Exception ex){
            return "Exception:\n"+ ex.getMessage();
        }
        return test;
    }

    @PostMapping("/move")
    public void listen(@RequestBody String dir){
        String[] dirArray=json_manager.toStringArray(dir);
        //System.out.println(dir);
        //System.out.println(dirArray[1]);
        String command="";

        if(dirArray[1].equals("FWLT")||dirArray[1].equals("FWRT")||dirArray[1].equals("BWLT")||dirArray[1].equals("BWRT")){
             command="MOVE:"+dirArray[1]+":"+speed+",45,RS";
        }else if(dirArray[1].equals("TRRT")||dirArray[1].equals("TRLT")){
            command="MOVE:"+dirArray[1]+":"+ Math.round(speed/2)+",000,RS";
        }else{
             command="MOVE:"+dirArray[1]+":"+speed+",000,RS";
        }
        System.out.println(";"+command);
        mBot.send(";"+command);
    }

    @GetMapping("/mbot_selection")
    public ArrayList<String> mbotSelection(){
        return MBotListener.getDevices();
    }

    @PostMapping("/color")
    public void ledColor(@RequestBody String colors){
        System.out.println(colors);

        String[] dirLedColor= json_manager.toStringArray(colors);
        char[] hex=dirLedColor[1].toCharArray();
        String command="MISC:LEDS:"+String.valueOf(hex[1]).toUpperCase()+String.valueOf(hex[2]).toUpperCase()+","+String.valueOf(hex[3]).toUpperCase()+String.valueOf(hex[4]).toUpperCase()+","+String.valueOf(hex[5]).toUpperCase()+String.valueOf(hex[6]).toUpperCase()+","+dirLedColor[3];
        System.out.println(";"+command);
        mBot.send(";"+command);
    }
}