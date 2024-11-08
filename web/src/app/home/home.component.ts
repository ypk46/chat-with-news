import { Component, inject } from '@angular/core';
import { Article, ArticleService } from '../article.service';
import { DatePipe, NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    NgIf,
    MatCardModule,
    DatePipe,
    FormsModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent {
  articles: Article[] = [];
  chosenArticle: Article | null = null;
  articleService = inject(ArticleService);
  currentIndex = 0;
  hasNextArticle = true;
  hasPreviousArticle = true;
  query = '';
  answer = '';
  loading = false;

  constructor() {
    this.articleService.getArticles().then((response) => {
      this.articles = response.data;
      this.chosenArticle = this.articles[this.currentIndex];
      this.hasPreviousArticle = false;
    });
  }

  changeArticle(idx: number) {
    this.currentIndex += idx;
    this.chosenArticle = this.articles[this.currentIndex];
    this.hasPreviousArticle = this.currentIndex > 0;
    this.hasNextArticle = this.currentIndex < this.articles.length - 1;
  }

  search() {
    if (this.query) {
      this.loading = true;
      this.articleService
        .queryArticles(this.query)
        .then((data) => {
          const article = this.articles.find(
            (article) => article.id === data.response.article_id
          );

          if (article) this.chosenArticle = article;

          this.answer = data.response.answer;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
}
