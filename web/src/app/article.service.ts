import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';

export interface Article {
  content: string;
  created_at: string;
  title: string;
  id: number;
  published_at: string;
  summary: string;
  link: string;
  feed_name: string;
  feed_image: string;
}

@Injectable({
  providedIn: 'root',
})
export class ArticleService {
  url: string;

  constructor() {
    this.url = environment.apiUrl;
  }

  getArticles(date: string) {
    return fetch(`${this.url}/articles?date=${date}`).then(
      (response) => <Promise<{ data: Article[] }>>response.json()
    );
  }

  queryArticles(query: string, date: string) {
    return fetch(`${this.url}/chats`, {
      method: 'POST',
      body: JSON.stringify({ query, date }),
      headers: {
        'Content-Type': 'application/json',
      },
    }).then(
      (response) =>
        <Promise<{ answer: string; article_id: number }>>response.json()
    );
  }
}
