import Handlebars from 'handlebars'

export function generateHtml() {
  // Get a reference to the template source
  const templateSource = `
  <html>
    <body style="background-color: grey;">
      <h1>Test</h1>
      <h1>{{ title }}</h1><p>{{ body }}</p>
    </body>
  </html>
`
  // Compile the template
  const template = Handlebars.compile(templateSource)

  // Define the data to be used in the template
  const data = {
    title: 'My Title',
    body: 'This is the body of my template.'
  }

  // Render the template with the data
  const renderedTemplate = template(data)
  return renderedTemplate
}

// const generateHtml = (path, sourceFileContents, scrollTo = null, lineTo = null) => {
//   const pathExtension = path.substring(path.lastIndexOf('.'))
//   const langMap = {
//     '.html': 'html',
//     '.css': 'css',
//     '.js': 'javascript',
//     '.py': 'python',
//     '.java': 'java',
//     '.md': 'markdown'
//     // Add more mappings for other file types as needed
//   }
//   const lang = langMap[pathExtension] || 'auto'

//   const scrollPosX = scrollTo?.x || 0
//   const scrollPosY = scrollTo?.y || 0

//   const jsFileTemplate = environment.getTemplate('template.jinja-js')
//   const jsFileContents = jsFileTemplate.render({
//     scroll_to: scrollTo,
//     scroll_to_x: scrollPosX,
//     line_to: lineTo
//   })

//   const template = environment.getTemplate('template.html')
//   const htmlStr = template.render({
//     lang,
//     source_file_contents: sourceFileContents,
//     js_file_contents: jsFileContents
//   })

//   if (htmlDebug) {
//     const fs = require('fs')
//     fs.writeFileSync('junk-content.html', htmlStr)
//   }

// //   return htmlStr
// }

export function generateHtml_OFFLINE() {
  // return a dummy html file for testing
  return `
  <html>
    <body style="background-color: grey;">
      <h1>Test</h1>
    </body>
  </html>
`
}
