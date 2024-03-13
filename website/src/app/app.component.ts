import { HttpClient } from '@angular/common/http';
import { Component, OnInit, HostListener } from '@angular/core';
import { DataService } from './data.service';
import { MbotSelection } from './mbot-selection.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',

  
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  receivedMessage: string = '';
  mBotIpAddress: string = '';
  speed: number = 0;
  sensorData: string = '';
  mbotSelection: MbotSelection[] = [];

  constructor(private dataService: DataService, private http: HttpClient) { }

  ngOnInit() {
    this.fetchData();
    this.fetchSensorData();
    this.fetchMbotSelection();
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

  saveIpAddress() {
    console.log('mBot IP Address:', this.mBotIpAddress);
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
  handleKeyboardEvent(event: KeyboardEvent) {
    switch (event.key) {
      case 'w':
        this.sendControlCommand('F');
        break;
      case 'a':
        this.sendControlCommand('L');
        break;
      case 's':
        this.sendControlCommand('B');
        break;
      case 'd':
        this.sendControlCommand('R');
        break;
    }
  }

  sendControlCommand(direction: string) {
    this.http.post('http://10.10.2.120:6968/direction', { direction }).subscribe(
      () => console.log('Control command sent successfully.'),
      error => console.error('Error sending control command:', error)
    );
  }

  fetchSensorData() {
    this.dataService.fetchSensorData().subscribe(
      (data: any) => {
        if (typeof data === 'string') {
          this.sensorData = data || 'No message received';
        } else if (typeof data === 'object' && 'message' in data) {
          this.sensorData = data.message || 'No message received';
        } else {
          this.sensorData = 'Invalid message format';
        }
        console.log('Received Message:', this.sensorData);
      },
      error => {
        console.error('Error fetching message:', error);
        this.sensorData = 'Error fetching message';
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
}
