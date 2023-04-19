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

export function generateHtml() {
  // return a dummy html file for testing
  return '<html><body><h1>Test</h1></body></html>'
}
