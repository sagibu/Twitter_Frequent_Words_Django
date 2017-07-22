import { Component } from '@angular/core';
import { Http, Response } from '@angular/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {
  words: String[];
  num_of_words: Number;
  constructor(private http: Http){
	this.http.request('http://127.0.0.1:8000/count/abcd').subscribe((res: Response) => {
                console.log(res.json());
                this.words = res.json();
        });
	this.http.request('http://127.0.0.1:8000/topic_data/abcd').subscribe((res: Response) => {
		console.log(res.json());
		this.num_of_words = res.json().num_of_words;
	});

}
  title = 'bla';
}
