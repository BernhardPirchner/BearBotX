package BBX.BearBotX;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.core.task.SimpleAsyncTaskExecutor;
import org.springframework.core.task.TaskExecutor;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class BearBotX_Application {

	public static void main(String[] args) {
		SpringApplication.run(BearBotX_Application.class, args);
	}

	@Bean
	public TaskExecutor taskExecutor(){
		return new SimpleAsyncTaskExecutor();
	}
}
