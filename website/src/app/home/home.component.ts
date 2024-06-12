import { HttpClient } from '@angular/common/http';
import { Component, OnInit, HostListener } from '@angular/core';
import { DataService } from '../data.service';
import { MbotSelection } from '../mbot-selection.model';
import { Router } from '@angular/router';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})

export class HomeComponent {
  mBotIpAddress: string = '';
  mbotSelection: MbotSelection[] = [];
  constructor(private dataService: DataService, private http: HttpClient, private router: Router) { }

  saveIpAddress() {
    console.log('mBot IP Address:', this.mBotIpAddress);
    this.connectToIpAddress();
    this.router.navigate(['/app-extension']);
  }

  connectToIpAddress() {
    console.log('mBot IP Address:', this.mBotIpAddress);
    const url = 'http://10.10.2.120:6968/connect';
    this.http.post(url, { ipAddress: this.mBotIpAddress }).subscribe(
      (response) => {
        console.log('Successfully connected to mBot', response);
        //this.ext.isConnected = true;
      },
      (error) => {
        console.error('Error connecting to mBot:', error);
      }
    );
  }
}
