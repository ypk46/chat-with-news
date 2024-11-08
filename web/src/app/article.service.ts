import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';

export interface Article {
  author: string;
  content: string;
  created_at: string;
  title: string;
  id: number;
  published_at: string;
  summary: string;
}

@Injectable({
  providedIn: 'root',
})
export class ArticleService {
  url: string;

  constructor() {
    this.url = environment.apiUrl;
  }

  getArticles() {
    return fetch(`${this.url}/articles`).then(
      (response) => <Promise<{ data: Article[] }>>response.json()
    );
  }

  queryArticles(query: string) {
    return fetch(`${this.url}/chats`, {
      method: 'POST',
      body: JSON.stringify({ query }),
      headers: {
        'Content-Type': 'application/json',
      },
    }).then(
      (response) =>
        <Promise<{ response: { answer: string; article_id: number } }>>(
          response.json()
        )
    );
  }
}
