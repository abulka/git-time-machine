export class Commit {
  id: number
  sha: string
  date: string
  author: string
  comment: string

  constructor(id: number, sha: string, date: string, author: string, comment: string) {
    this.id = id
    this.sha = sha
    this.date = date
    this.author = author
    this.comment = comment
  }
}
