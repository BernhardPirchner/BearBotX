import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';
import { map } from 'rxjs/operators';
import { MbotSelection } from './mbot-selection.model';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private http: HttpClient) { }

  fetchMessage(): Observable<string> {
    return this.http.get('http://10.10.2.120:6968/test', { responseType: 'text' });
  }

  fetchSensorData(): Observable<any> {
    return this.http.get('http://10.10.2.120:6968/sensor_data', { responseType: 'text' });
  }
  
  sendSpeed(speed: number): Observable<any> {
    return this.http.post('http://10.10.2.120:6968/velocity', { speed });
  }
  
  fetchMbotSelection(): Observable<MbotSelection[]> {
    return this.http.get<string[]>('http://10.10.2.120:6968/mbot_selection').pipe(
      map((data: string[]) => {
        return data.map(item => {
          const [name, ipAddress] = item.split(', ');
          return { name, ipAddress } as MbotSelection;
        });
      })
    );
  }

  fetchLightSensorData(): Observable<number[]> {
    return this.http.get<number[]>('http://10.10.2.120:6968/light_sensor');
  }
}