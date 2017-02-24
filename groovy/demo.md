base 64
```groovy
"hello".getBytes().encodeBase64().toString()
```
html
```groovy
new URL("http://www.google.com").openConnection().with {
    setRequestProperty("Header", "value")
    setRequestMethod("POST")
    setDoOutput(true)
    inputStream.text  // getInputStream().text
    responseCode      // getResponseCode()
    responseMessage   // getResponseMessage()
}
```
short version
```groovy
new URL("http://www.google.com").openStream().text
```

xml
```groovy
new MarkupBuilder().langs(type:"current") {
    language("Java")
    language("Groovy")
    language("JavaScript")
}

// output
<langs type='current'>
  <language>Java</language>
  <language>Groovy</language>
  <language>JavaScript</language>
</langs>
```

all in one line
```groovy
import groovy.xml.StreamingMarkupBuilder

def xml = new StreamingMarkupBuilder().bind {
    ShortMessage() {
        sendSort("SMS")
        sendType("COMMON_GROUP")
        isGroup("1")
    }
}
```

json
```groovy
new JsonSlurper().parseText('{ "name": "John Doe" })
```
