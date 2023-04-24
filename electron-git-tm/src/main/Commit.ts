export class Commit {
  sha: string;
  date: string;
  author: string;
  comment: string;

  constructor(sha: string, date: string, author: string, comment: string) {
    this.sha = sha;
    this.date = date;
    this.author = author;
    this.comment = comment;
  }
}
