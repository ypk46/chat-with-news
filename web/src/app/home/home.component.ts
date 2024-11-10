import { Component, inject } from '@angular/core';
import { Article, ArticleService } from '../article.service';
import { DatePipe, CommonModule } from '@angular/common';
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
    CommonModule,
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
  query = '';
  answer = '';
  loading = false;
  date = new Date();

  constructor() {
    this.articleService
      .getArticles(<string>this.formatDate(this.date))
      .then((response) => {
        this.articles = response.data;
      });
  }

  /**
   * Format date to YYYY-MM-DD string.
   */
  formatDate(date: Date) {
    return new DatePipe('en-US').transform(date, 'yyyy-MM-dd');
  }

  /**
   * Change current date attribute based on the action.
   * @param action - 'next' or 'previous'
   */
  changeDate(action: string) {
    if (action === 'next') {
      this.date.setDate(this.date.getDate() + 1);
    } else {
      this.date.setDate(this.date.getDate() - 1);
    }

    // Reload the date
    this.date = new Date(this.date);

    this.articleService
      .getArticles(<string>this.formatDate(this.date))
      .then((response) => {
        this.articles = response.data;
      });
  }

  /**
   * Go to a specific link in a blank page.
   * @param link - URL to go to
   */
  goTo(link: string) {
    window.open(link, '_blank');
  }

  search() {
    if (this.query) {
      this.loading = true;
      this.answer = '';
      this.chosenArticle = null;

      this.articleService
        .queryArticles(this.query, <string>this.formatDate(this.date))
        .then((data) => {
          const match = this.articles.find(
            (article) => article.id === data.article_id
          );
          if (match) this.chosenArticle = match;
          this.answer = data.answer;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
}
