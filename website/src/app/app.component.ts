import { HttpClient } from '@angular/common/http';
import { Component, OnInit, HostListener } from '@angular/core';
import { DataService } from './data.service';
import { MbotSelection } from './mbot-selection.model';
import { interval } from 'rxjs';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  receivedMessage: string = '';
  mBotIpAddress: string = '';
  speed: number = 0;
  //sensorData: string = '';
  sensorData: string[] = [];
  mbotSelection: MbotSelection[] = [];
  colors: string[] = ['#e66465', '#e66465', '#e66465', '#e66465', '#e66465'];
  intervalId: any;
  applySameColor: boolean = false;
  pressedKeys: Set<string> = new Set<string>();
  combinedCommand: string = '';
  lightSensorData: number[] = [];

  constructor(private dataService: DataService, private http: HttpClient) { }

  ngOnInit() {
    this.fetchData();
    this.fetchSensorData();
    this.fetchMbotSelection();
    interval(2000).subscribe(() => {
      this.fetchSensorData();
    });
  }

  fetchData() {
    this.dataService.fetchMessage().subscribe(
      (data: any) => {
        if (typeof data === 'string') {
          this.receivedMessage = data || 'No message received';
        } else if (typeof data === 'object' && 'message' in data) {
          this.receivedMessage = data.message || 'No message received';
        } else {
          this.receivedMessage = 'Invalid message format';
        }
        console.log('Received Message:', this.receivedMessage);
      },
      error => {
        console.error('Error fetching message:', error);
        this.receivedMessage = 'Error fetching message';
      }
    );
  }

  connectToIpAddress() {
    console.log('mBot IP Address:', this.mBotIpAddress);
    const url = 'http://10.10.2.120:6968/connect';
    this.http.post(url, { ipAddress: this.mBotIpAddress }).subscribe(
      (response) => {
        console.log('Successfully connected to mBot', response);
      },
      (error) => {
        console.error('Error connecting to mBot:', error);
      }
    );
  }

  disconnectFromIpAddress() {
    const url = 'http://10.10.2.120:6968/disconnect';
    this.http.post(url, { ipAddress: this.mBotIpAddress }).subscribe(
      (response) => {
        console.log('Successfully disconnected from mBot', response);
        this.mBotIpAddress = '';
      },
      (error) => {
        console.error('Error disconnecting from mBot:', error);
      }
    );
  }

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

    this.updateCombinedCommand();

    if (!this.intervalId && this.combinedCommand) {
      this.intervalId = setInterval(() => {
        if (this.combinedCommand) {

          const formattedCommand = this.convertCombinedCommand(this.combinedCommand);
          this.sendControlCommand(formattedCommand);
        }
      }, 200);
    }
  }

  @HostListener('document:keyup', ['$event'])
  handleKeyUpEvent(event: KeyboardEvent) {
    this.pressedKeys.delete(event.key);

    this.updateCombinedCommand();

    if (this.pressedKeys.size === 0 || !this.combinedCommand) {
      clearInterval(this.intervalId);
      this.intervalId = null;
      if(!this.combinedCommand) {
        this.sendControlCommand('STOP');
      }
    }
  }

  updateCombinedCommand() {
    this.combinedCommand = '';

    if (this.pressedKeys.has('w')) this.combinedCommand += 'Forward';
    if (this.pressedKeys.has('s')) this.combinedCommand += 'Backward';
    if (this.pressedKeys.has('a')) this.combinedCommand += 'Left';
    if (this.pressedKeys.has('d')) this.combinedCommand += 'Right';
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
      (data: number[]) => {
        this.lightSensorData = data;
      },
      error => {
        console.error('Error fetching light sensor data:', error);
      }
    );
  }

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

  sendColorToServer(color: string, ledNumber: number) { //s
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
