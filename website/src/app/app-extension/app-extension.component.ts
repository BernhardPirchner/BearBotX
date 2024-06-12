import {Component, OnInit, HostListener, AfterViewInit } from '@angular/core';
import { DataService } from '../data.service';
import { MbotSelection } from '../mbot-selection.model';
import { HttpClient } from '@angular/common/http';
import { interval } from 'rxjs';
 
@Component({
  selector: 'app-root',
  templateUrl: './app-extension.component.html',
  styleUrls: ['./app-extension.component.css'],
})
export class AppExtensionComponent implements OnInit {
 
  mBotIpAddress: string = '';
  isConnected: boolean = false;
  speed: number = 0;
  sensorData: string[] = [];
  mbotSelection: MbotSelection[] = [];
  intervalId: any;
  applySameColor: boolean = false;
  pressedKeys: Set<string> = new Set<string>();
  combinedCommand: string = '';
  lightSensorData: boolean[] = [];
 
  safetyStatus: boolean = true;
  autopilotStatus: boolean = true;
 
  colors: string[] = ['#e66465', '#e66465', '#e66465', '#e66465', '#e66465'];
 
  constructor(private dataService: DataService, private http: HttpClient) { }
 
  ngOnInit() {
    console.log('ngoninit called');
    this.fetchSensorData();
    this.fetchMbotSelection();
    //this.fetchSafetyStatus();
    //this.fetchAutopilotStatus();
    interval(2000).subscribe(() => {
      this.fetchSensorData();
    });
    interval(500).subscribe(() => {
      this.fetchLightSensorData();
    });
  }
 
  toggleConnection() {
    if (this.isConnected) {
      //this.disconnectFromIpAddress();
    } else {
      this.connectToIpAddress();
    }
  }
 
  /*toggleSafetyStatus() {
    if (this.safetyStatus) {
      this.safetyStatus = !this.safetyStatus;
    } else {
      this.fetchSafetyStatus();
    }
  }
 
  toggleAutopilotStatus() {
    if (this.autopilotStatus) {
      this.autopilotStatus = !this.autopilotStatus;
    } else {
      this.fetchAutopilotStatus();
    }
  }*/
 
  //bis zeile 110 andere variante bzgl. safety/autopilot mode (mit post ?)

  toggleSafetyStatus() {
    if (this.safetyStatus) {
      this.safetyStatus = false;
      this.updateSafetyStatusOnServer(false);
    } else {
      this.safetyStatus = true;
      this.updateSafetyStatusOnServer(true);
    }
  }
 
  toggleAutopilotStatus() {
    if (this.autopilotStatus) {
      this.autopilotStatus = false;
      this.updateAutopilotStatusOnServer(false);
    } else {
      this.autopilotStatus = true;
      this.updateAutopilotStatusOnServer(true);
    }
  }
 
 
  updateSafetyStatusOnServer(status: boolean) {
    this.dataService.updateSafetyStatus(status).subscribe(
      () => {
        console.log('Safety status updated successfully');
      },
      error => {
        console.error('Error updating safety status:', error);
      }
    );
  }
 
  updateAutopilotStatusOnServer(status: boolean) {
    this.dataService.updateAutopilotStatus(status).subscribe(
      () => {
        console.log('Autopilot status updated successfully');
      },
      error => {
        console.error('Error updating autopilot status:', error);
      }
    );
  }
 
 
  connectToIpAddress() {
    console.log('mBot IP Address:', this.mBotIpAddress);
    const url = 'http://10.10.2.120:6968/connect';
    this.http.post(url, { ipAddress: this.mBotIpAddress }).subscribe(
      (response) => {
        console.log('Successfully connected to mBot', response);
        this.isConnected = true;
      },
      (error) => {
        console.error('Error connecting to mBot:', error);
      }
    );
  }
 
  /*disconnectFromIpAddress() {
    this.dataService.disconnectFromIpAddress(this.mBotIpAddress).subscribe(
      (response) => {
        console.log('Successfully disconnected from mBot', response);
        this.isConnected = false;
        this.mBotIpAddress = '';
      },
      (error) => {
        console.error('Error disconnecting from mBot:', error);
      }
    );
  }*/
 
  updateSpeed() {
    console.log('Speed:', this.speed);
    this.dataService.sendSpeed(this.speed).subscribe(
      (response: any) => {
        console.log('Speed sent successfully:', response);
      },
      error => {
        console.error('Error sending speed:', error);
      }
    );
  }
 
  @HostListener('document:keydown', ['$event'])
  handleKeyDownEvent(event: KeyboardEvent) {
    this.pressedKeys.add(event.key);
 
    /*this.updateCombinedCommand();
 
    if (!this.intervalId && this.combinedCommand) {
      this.intervalId = setInterval(() => {
        if (this.combinedCommand) {
 
          const formattedCommand = this.convertCombinedCommand(this.combinedCommand);
          this.sendControlCommand(formattedCommand);
        }
      }, 200);
    }*/
    if (this.pressedKeys.size > 2) {
      this.pressedKeys.delete([...this.pressedKeys][0]);
    }
 
    // Update the combined command
    this.updateCombinedCommand();
  }
 
  @HostListener('document:keyup', ['$event'])
  handleKeyUpEvent(event: KeyboardEvent) {
    /*this.pressedKeys.delete(event.key);
 
    this.updateCombinedCommand();
 
    if (this.pressedKeys.size === 0 || !this.combinedCommand) {
      clearInterval(this.intervalId);
      this.intervalId = null;
      if(!this.combinedCommand) {
        this.sendControlCommand('STOP');
      }
    }*/
    this.pressedKeys.delete(event.key);
 
    this.updateCombinedCommand();
  }
 
  updateCombinedCommand() {
    this.combinedCommand = '';
 
    this.pressedKeys.forEach(key => {
      switch (key) {
        case 'w':
          this.combinedCommand += 'Forward';
          break;
        case 's':
          this.combinedCommand += 'Backward';
          break;
        case 'a':
          this.combinedCommand += 'Left';
          break;
        case 'd':
          this.combinedCommand += 'Right';
          break;
        default:
          break;
      }
    });
 
    if (this.combinedCommand) {
      const formattedCommand = this.convertCombinedCommand(this.combinedCommand);
      this.sendControlCommand(formattedCommand);
    } else {
      this.sendControlCommand('STOP');
    }
  }
 
  convertCombinedCommand(combinedCommand: string): string {
    switch (combinedCommand) {
      case 'ForwardLeft':
        return 'FWLT';
      case 'ForwardRight':
        return 'FWRT';
      case 'BackwardLeft':
        return 'BWLT';
      case 'BackwardRight':
        return 'BWRT';
      case 'Forward':
        return 'FWST';
      case 'Left':
        return 'TRLT';
      case 'Right':
        return 'TRRT';
      case 'Backward':
        return 'BWST';
      default:
        return combinedCommand;
    }
  }
 
  sendControlCommand(direction: string) {
    this.http.post('http://10.10.2.120:6968/move', { direction }).subscribe(
      () => console.log('Control command sent successfully.'),
      error => console.error('Error sending control command:', error)
    );
  }
 
  fetchSensorData() {
    this.dataService.fetchSensorData().subscribe(
      (data: string[]) => {
        this.sensorData = data;
        console.log('Received Sensor Data:', this.sensorData);
      },
      error => {
        console.error('Error fetching sensor data:', error);
        this.sensorData = [];
      }
    );
  }
 
  fetchMbotSelection() {
    this.dataService.fetchMbotSelection().subscribe(
      (data: MbotSelection[]) => {
        this.mbotSelection = data;
        console.log('Mbot Selection:', this.mbotSelection);
      },
      error => {
        console.error('Error fetching Mbot selection:', error);
      }
    );
  }
 
  fetchLightSensorData() {
    this.dataService.fetchLightSensorData().subscribe(
      (data: boolean[]) => {
        console.log('Received Light Sensor Data:', this.lightSensorData);
        this.lightSensorData = data;
      },
      error => {
        console.error('Error fetching light sensor data:', error);
      }
    );
  }
 
  fetchSafetyStatus() {
    this.dataService.fetchSafetyStatus().subscribe(
      (response) => {
        console.log('Successful Safety', response);
        this.safetyStatus = false;
    },
    (error) => {
      console.log('Error Safety', error);
    }
    );
  }
 
  fetchAutopilotStatus() {
    this.dataService.fetchAutopilotStatus().subscribe(
      (status: boolean) => {
        this.autopilotStatus = status;
        console.log('Autopilot Status:', this.autopilotStatus ? 'ON' : 'OFF');
      },
      (response) => {
          console.log('Successful Autopilot', response);
          this.autopilotStatus = false;
      }
    );
  }
 
  /*fetchSafetyStatus() {
    this.dataService.fetchSafetyStatus().subscribe(
      (data: any) => {
        this.safetyStatus = data;
        console.log('Safety Status:', this.safetyStatus);
      },
      error => {
        console.error('Error fetching safety status:', error);
        this.safetyStatus = 'Error';
      }
    );
  }*/
 
  /*fetchAutopilotStatus() {
    this.dataService.fetchAutopilotStatus().subscribe(
      (data: any) => {
        this.autopilotStatus = data;
        console.log('Autopilot Status:', this.autopilotStatus);
      },
      error => {
        console.error('Error fetching autopilot status:', error);
        this.autopilotStatus = 'Error';
      }
    );
  }*/
 
  onColorChanged(event: any, ledNumber: number) {
    const color = event.target.value;
    this.colors[ledNumber - 1] = color;
 
    if (this.applySameColor) {
      this.updateAllColors(color);
    } else {
      this.sendColorToServer(color, ledNumber);
    }
  }
 
  updateAllColors(color: string) {
    this.colors = Array(5).fill(color);
    this.sendColorToServer(color, 0);
  }
 
  sendColorToServer(color: string, ledNumber: number) {
    const formattedLedNumber = ledNumber.toString().padStart(2, '0')
    const url = 'http://10.10.2.120:6968/color';
    this.http.post(url, { color, ledNumber: formattedLedNumber }).subscribe(
      (response) => {
        console.log('Colors sent to server successfully:', response);
      },
      (error) => {
        console.error('Error sending colors to server:', error);
      }
    );
  }
}