/// <reference types="electron-vite/node" />
import Handlebars from 'handlebars'
import fs from 'fs'
import { getFileContents as getFileContent } from './getFileContent'
import { isBinary } from 'istextorbinary'
import { fileExtToPrismAlias } from './fileExtToPrismAlias'
import t1 from '../../resources/templates/template-file-contents-autoload.hbs?asset'
import t2 from '../../resources/templates/template-file-js.hbs?asset'

export interface Point {
  x: number
  y: number
}

// const templateSource = fs.readFileSync('src/main/templates/template-file-contents.hbs', 'utf8')
const templateSource = fs.readFileSync(t1, 'utf8')
const template = Handlebars.compile(templateSource) // Compile the template

const templateSourceJs = fs.readFileSync(t2, 'utf8')
const templateJs = Handlebars.compile(templateSourceJs) // Compile the js template

export function generateHtml(
  commit,
  path,
  scrollTo: Point | null = null,
  lineTo: number | null
): string {
  const scrollPosX = scrollTo?.x || 0
  const scrollPosY = scrollTo?.y || 0

  const source_file_contents: string = getFileContent(commit, path)
  const source_file_contents_buffer = Buffer.from(source_file_contents)
  const isBinaryFile = isBinary(null, source_file_contents_buffer)
  if (isBinaryFile) {
    return 'Binary file'
  }

  const lang = fileExtToPrismAlias(path)

  // highlight.js auto-detection is not working for some files so help it by
  // using the file extension to set the language-* if possible
  const lang_override = lang != '' ? `lang-${lang}` : ''

  const jsFileTemplate = constructJsFileContents(templateJs, scrollPosX, scrollPosY, lineTo)

  // Define the data to be used in the template
  const data = {
    title: 'My Title',
    body: 'This is the body of my template.',
    lang: lang,
    lang_override: lang_override,
    vers: '1.29.0', // https://cdnjs.com/libraries/prism/1.29.0
    source_file_contents: source_file_contents,
    js_file_contents: jsFileTemplate // '' // 'console.log("Hello World from template")'
  }

  // Render the template with the data
  const renderedTemplate = template(data)
  return renderedTemplate
}

function constructJsFileContents(
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  templateJs: Handlebars.TemplateDelegate<any>,
  scrollPosX: number,
  scrollPosY: number,
  lineTo: number | null
): string {
  const data = {
    scroll_to: scrollPosY,
    scroll_to_x: scrollPosX,
    line_to: lineTo
  }
  const jsFileContents = templateJs(data)
  return jsFileContents
}