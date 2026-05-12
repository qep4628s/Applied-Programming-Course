# Work Log

**Student Name:** 

Instructions: Fill out one log for each course day. Content to consider: Course Sessions + Assignment

## Template:

---

## 1. ✅ What did I accomplish?

_Reflect on the activities, exercises, and work you completed today._

**Guiding questions:**
- What topics or concepts did you work with?
- What exercises or projects did you complete?
- What tools or technologies did you use?
- What did you learn or practice?



---

## 2. 🚧 What challenges did I face?

_Describe any difficulties, obstacles, or confusing moments you encountered._

**Guiding questions:**
- What was difficult to understand?
- Where did you get stuck?
- What errors or problems did you face?
- What felt frustrating or confusing?




---

## 3. 💡 How did I overcome them?

_Explain how you overcame the challenges or what help you needed._

**Guiding questions:**
- What strategies did you try?
- Who or what helped you (instructor, classmates, documentation)?
- What did you learn from solving the problem?
- What questions do you still have?


---

## Week 1

### Day 1

#### 1. ✅ What did I accomplish?
Am ersten Tag ging es hauptsächlich um die Einrichtung der Arbeitsumgebung. Ich habe Git, VS Code und `uv` installiert und überprüft, ob alles richtig funktioniert. Dieser Teil war für mich nicht besonders schwierig, und ich bin damit gut zurechtgekommen.

Außerdem habe ich die Grundlagen wiederholt, zum Beispiel was eine API ist, wofür FastAPI benutzt wird und wie ein einfacher Endpoint funktioniert. Ich habe einfache Endpoints wie `/`, `/status` und `/about` erstellt und in `/docs` getestet.

Die zusätzlichen Übungen mit einfachen Berechnungen, zum Beispiel `/square/{number}` und `/double/{number}`, habe ich auch umgesetzt. Diese Aufgaben waren für mich gut verständlich, deshalb habe ich in diesem Teil nicht sehr viel Hilfe von OpenAI gebraucht.
---

#### 2. 🚧 What challenges did I face?
Eine sehr große Herausforderung gab es an diesem Tag für mich nicht. Die Aufgaben waren grundsätzlich verständlich, aber ich musste mich noch an die genaue Schreibweise gewöhnen.Manchmal war ich unsicher, wo ich ein Komma setzen muss, wo ein Slash `/` hingehört oder wie die Klammern richtig geschrieben werden. Auch bei den URLs und Endpoints musste ich genauer aufpassen, damit ich zum Beispiel `/status` oder `/square/{number}` richtig schreibe.Es waren also eher kleinere Syntax- und Schreibfehler, aber keine Probleme, die ich gar nicht lösen konnte.
---

#### 3. 💡 How did I overcome them?
Ich habe bei Unsicherheiten ChatGPT gefragt und mir die Schreibweise Schritt für Schritt erklären lassen. Danach habe ich die Beispiele noch einmal selbst ausprobiert und mehrere kleine Übungen gemacht.Durch das wiederholte Schreiben und Testen der Endpoints habe ich besser verstanden, wo Kommas, Slashes und Klammern hingehören. Dadurch wurden die kleinen Fehler mit der Zeit weniger.
---

### Day 2

#### 1. ✅ What did I accomplish?
Am zweiten Tag habe ich gelernt, wie man mit verschiedenen HTTP-Methoden arbeitet, zum Beispiel `POST`, `GET`, `PUT` und `DELETE`. Ich habe besser verstanden, dass diese Methoden unterschiedliche Aufgaben haben und nicht einfach austauschbar sind.

Besonders wichtig war für mich der Unterschied zwischen Daten abrufen und Daten erstellen oder verändern. `GET` benutzt man, um Daten zu lesen, `POST` um neue Daten zu erstellen, `PUT` um bestehende Daten zu aktualisieren und `DELETE` um Daten zu löschen.

Außerdem habe ich angefangen, diese Methoden in meiner Note API anzuwenden und besser zu verstehen, wie die Endpoints aufgebaut sind und wie man sie in `/docs` testen kann.
---

#### 2. 🚧 What challenges did I face?
Der ganze Themenbereich war für mich eine Herausforderung. Ich habe zwar verstanden, dass `GET`, `POST`, `PUT` und `DELETE` jeweils für unterschiedliche Aufgaben benutzt werden, aber trotzdem hatte ich noch das Gefühl, dass ich das Gesamtkonzept nicht komplett verstanden habe.

Besonders verwirrend war für mich, wie die einzelnen Endpoints zusammenhängen und wann genau welche Methode benutzt werden soll. Ich konnte die Beispiele nachvollziehen, aber wenn ich selbst entscheiden musste, welche Methode oder welcher Endpoint passt, war ich noch unsicher.

Es war also nicht ein einzelner Fehler im Code, sondern eher das allgemeine Verständnis von API-Struktur und HTTP-Methoden, das für mich noch schwierig war.
---

#### 3. 💡 How did I overcome them?
Durch die Übungen und das Ausprobieren der Endpoints in `/docs` habe ich das Thema etwas besser verstanden. Besonders geholfen hat mir, die Methoden direkt in der API auszuprobieren und zu sehen, welche Antwort zurückkommt.

Trotzdem würde ich nicht sagen, dass ich diese Schwierigkeiten schon komplett überwunden habe. Ich verstehe die Grundidee jetzt besser, aber ich merke, dass ich noch mehr Übung brauche, um sicherer zu werden. Ich glaube, dass dieses Thema vor allem Zeit und Wiederholung braucht.
---

### Day 3

#### 1. ✅ What did I accomplish?

Am dritten Tag habe ich weiter an meiner Note API gearbeitet und versucht, die API aus Day 2 zu erweitern. Ich habe mich mehr mit REST API Design beschäftigt und wiederholt, dass Endpoints sinnvoll und ressourcenorientiert aufgebaut sein sollten.

Außerdem habe ich den Unterschied zwischen Path Parameters und Query Parameters besser verstanden.

Ich habe meine Note API um weitere Funktionen erweitert, zum Beispiel Kategorien, Tags, Filter, `PUT`, `PATCH` und `DELETE`. Außerdem habe ich zusätzliche Endpoints wie `/tags`, `/categories` und `/notes/stats` ergänzt.

Da ich die Vorlesungen immer mit chatgpt lerne, kannte ich einige Grundlagen schon vorher. Das hat mir geholfen, manche Konzepte schneller einzuordnen und die Aufgaben besser zu verstehen.
---

#### 2. 🚧 What challenges did I face?
## 2. 🚧 What challenges did I face?

Eine Herausforderung war für mich, die API nicht nur nachzubauen, sondern wirklich zu verstehen, warum die Endpoints so aufgebaut sind. Bei Day 3 gab es viele neue Funktionen auf einmal, und dadurch war es manchmal schwer, den Überblick zu behalten.

Besonders bei den Filtern musste ich genauer nachdenken. Einzelne Filter wie `category` oder `tag` waren noch verständlich, aber mehrere Filter gleichzeitig zu kombinieren war schwieriger. Ich musste darauf achten, dass die API nur die Notes zurückgibt, die wirklich zu allen Bedingungen passen.

Außerdem hatte ich mehrere kleine Fehler im Code. Zum Beispiel musste ich auf die richtige Reihenfolge der Endpoints achten, weil allgemeinere Routen wie `/notes/{note_id}` speziellere Routen stören können, wenn sie an der falschen Stelle stehen.

Auch die zusätzlichen Endpoints für Tags, Kategorien und Statistiken waren am Anfang ungewohnt. Ich habe ungefähr verstanden, was sie machen sollen, aber es war nicht immer sofort klar, wie ich die Daten dafür richtig sammeln und zurückgeben soll. Vor allem bei Listen und Dictionaries musste ich aufpassen, dass ich keine falschen Keys benutze und dass die Rückgabe zum jeweiligen Endpoint passt.

Insgesamt waren es keine riesigen Fehler, sondern eher viele kleine Stellen, bei denen ich genau hinschauen musste.
---

#### 3. 💡 How did I overcome them?
Ich habe versucht, die Probleme nicht alle auf einmal zu lösen, sondern Schritt für Schritt vorzugehen. Zuerst habe ich geprüft, ob die einfachen Endpoints funktionieren, und danach erst die schwierigeren Teile wie Filter, Tags, Kategorien und Statistiken getestet.

Bei den Filtern habe ich mehrere Beispiel-Notes erstellt und dann in `/docs` ausprobiert, ob die Ergebnisse stimmen. So konnte ich besser erkennen, ob ein Filter richtig funktioniert oder ob eine Note fälschlicherweise angezeigt oder übersprungen wird.

Bei den kleinen Fehlern im Code habe ich genauer auf die Struktur geachtet, zum Beispiel auf die Reihenfolge der Endpoints, die Einrückung und die richtigen Keys in Dictionaries. Wenn ein Endpoint nicht das richtige Ergebnis geliefert hat, habe ich die Rückgabe kontrolliert und den Code Stück für Stück angepasst.

Ich würde nicht sagen, dass ich alles sofort sicher beherrsche, aber durch das Testen und Korrigieren habe ich besser verstanden, wie die einzelnen Teile der API zusammenhängen.
---

## Week 2

### Day 4

#### 1. ✅ What did I accomplish?
Am vierten Tag habe ich mich zuerst mit `POST` Endpoints und Pydantic Models beschäftigt. Ich habe besser verstanden, dass `GET` zum Abrufen von Daten benutzt wird und `POST`, um neue Daten zu erstellen.

Ich habe die Course API aus der Vorlesung umgesetzt und die Modelle `CourseCreate` und `Course` erstellt. Danach habe ich `POST /courses` und `GET /courses` in `/docs` getestet. Dabei habe ich auch überprüft, ob die Daten in `courses.json` gespeichert werden, ob doppelte Course-Codes erkannt werden und ob fehlende Felder zu einem Fehler führen.

Danach habe ich mich mit `pytest` und `requests` beschäftigt. Ich habe zuerst einfache Tests für die Course API geschrieben und danach Tests für meine Note API aus Day 2 und Day 3 ergänzt. Am Ende hatte ich 18 Tests, die erfolgreich bestanden haben.
---

#### 2. 🚧 What challenges did I face?
Eine Schwierigkeit war, dass ich zum ersten Mal richtig mit `pytest` gearbeitet habe. Am Anfang war ich unsicher, wie ein Test überhaupt aufgebaut sein muss und was genau in einer Testfunktion geprüft werden soll.

Ich habe gemerkt, dass man beim Testen schnell kleine Fehler machen kann. Zum Beispiel kann man den falschen Endpoint aufrufen, einen falschen Status Code erwarten oder vergessen, dass der Server laufen muss, wenn man mit `requests` testet. Auch bei den `assert`-Zeilen war ich manchmal unsicher, weil ich nicht genau wusste, ob ich nur den Status Code prüfen soll oder auch den Inhalt der Antwort.

Außerdem war es ungewohnt, dass Fehler nicht nur im API-Code sein können, sondern auch im Test selbst. Wenn ein Test fehlschlägt, bedeutet das also nicht automatisch, dass der Endpoint falsch ist. Man muss auch kontrollieren, ob der Test richtig geschrieben wurde.
---

#### 3. 💡 How did I overcome them?
Ich habe zuerst mit sehr einfachen Tests angefangen, zum Beispiel nur zu prüfen, ob ein Endpoint den Status Code `200` oder `201` zurückgibt. Danach habe ich Schritt für Schritt weitere Prüfungen ergänzt, zum Beispiel ob die Antwort eine Liste ist oder ob bestimmte Felder wie `id`, `title` oder `created_at` vorhanden sind.

Wenn ein Test nicht funktioniert hat, habe ich zuerst geprüft, ob der Endpoint in `/docs` richtig funktioniert. Danach habe ich den Test selbst kontrolliert, zum Beispiel den Endpoint, die Testdaten und die erwarteten Status Codes.

Durch das wiederholte Ausführen mit `pytest` habe ich langsam besser verstanden, wie Tests aufgebaut sind und worauf man beim Schreiben von `assert` achten muss.
---

### Day 5

#### 1. ✅ What did I accomplish?
Heute habe ich die Validierung meiner Note API verbessert. Ich habe in main_day5.py die Modelle NoteCreate und NoteUpdate erweitert und mit Field, ConfigDict, field_validator und model_validator strengere Regeln eingebaut.

Ich habe gelernt, wie man Eingaben überprüft, bevor sie gespeichert werden. Zum Beispiel muss der Titel jetzt mindestens 3 Zeichen lang sein, die Kategorie muss zu den erlaubten Kategorien gehören und zusätzliche Felder wie tagz werden nicht mehr akzeptiert. Außerdem werden Kategorien und Tags normalisiert, zum Beispiel wird WORK zu work, doppelte Tags werden entfernt und ungültige Tags werden abgelehnt.

Danach habe ich die API in /docs getestet. Gültige Daten wurden mit 201 gespeichert und falsche Eingaben wurden mit 422 abgelehnt. Zusätzlich habe ich test_validation.py geschrieben und am Ende haben alle 8 Tests erfolgreich bestanden.
---

#### 2. 🚧 What challenges did I face?
Eine Herausforderung war, den Unterschied zwischen einfachen Regeln mit Field und eigenen Validatoren zu verstehen. Mindestlängen oder maximale Längen konnte ich direkt mit Field lösen, aber für Dinge wie erlaubte Kategorien, doppelte Tags oder das Umwandeln von WORK zu work brauchte ich eigene Validatoren.

Beim Schreiben der Tests hatte ich außerdem einen konkreten Fehler. Am Anfang haben 7 Tests bestanden, aber ein Test ist fehlgeschlagen. Der Test sollte prüfen, dass ein ungültiger Tag abgelehnt wird. Die API hat den Tag aber trotzdem akzeptiert und 201 zurückgegeben, obwohl ich 422 erwartet hatte.

Dadurch habe ich gemerkt, dass meine Tag-Validierung noch nicht streng genug war. Ich hatte zwar Tags in lowercase umgewandelt und Duplikate entfernt, aber ich hatte noch nicht geprüft, ob Tags nur erlaubte Zeichen enthalten. Besonders dieser Fehler hat mir gezeigt, dass ein bestandener Teil der Tests nicht automatisch bedeutet, dass die ganze Validierung vollständig ist.
---

#### 3. 💡 How did I overcome them?
Ich habe die Fehler Schritt für Schritt überprüft und dabei auch ChatGPT benutzt, um besser zu verstehen, warum ein Test fehlgeschlagen ist. Besonders bei dem Test mit dem ungültigen Tag hat mir ChatGPT geholfen zu erkennen, dass meine bisherige Validierung noch nicht streng genug war.

Danach habe ich die Tag-Validierung erweitert und ein Pattern ergänzt, damit Tags nur aus lowercase letters, Zahlen und Bindestrichen bestehen dürfen. Anschließend habe ich den Code nochmal gespeichert, den Server neu gestartet und die Tests erneut mit pytest ausgeführt.

Nach der Korrektur haben alle 8 Tests bestanden. Dadurch habe ich besser verstanden, dass Tests nicht nur Fehler anzeigen, sondern auch helfen, unvollständige Regeln in der Validierung zu finden.
---

### Day 6

#### 1. ✅ What did I accomplish?
Heute habe ich an der Test-Suite für meine Notes API gearbeitet. Außerdem habe ich geprüft, welche Teile von meinem Projekt noch fehlen oder verbessert werden müssen.

Zuerst habe ich die Datei test_main.py benutzt und die Tests mit pytest ausgeführt. Am Anfang haben nicht alle Tests funktioniert. Einige Fehler hatten mit Tags, Datum-Filtern und der SQLite-Datenbank zu tun.

Ich habe die Fehlermeldungen Schritt für Schritt gelesen und die Fehler in meiner API verbessert.
---

#### 2. 🚧 What challenges did I face?
Am Anfang haben nur ungefähr 50 von 70 Tests funktioniert. Ein konkreter Fehler war bei den Tags. In einem Test wurden Tags wie "URGENT", "urgent" und " meeting " an die API geschickt. Die Test-Suite erwartete, dass daraus nur saubere Tags wie `"urgent"
` und "meeting" werden.

Bei mir wurden die Tags am Anfang aber nicht richtig bereinigt. Teilweise blieben Großbuchstaben, Leerzeichen oder doppelte Tags erhalten.

Ein weiterer Fehler war bei den Datumsfiltern created_after und created_before. Wenn ein falsches Datum geschickt wurde, erwarteten die Tests den Status Code 422. Mein Code hat aber zuerst einen anderen Status Code zurückgegeben.

Außerdem gab es ein Problem bei /notes/stats, weil die Anzahl der Tags nicht immer zur Antwort von /tags gepasst hat.
---

#### 3. 💡 How did I overcome them?
Ich habe die Fehlermeldungen von pytest einzeln gelesen und danach die passenden Stellen in main.py geändert.

Für das Tag-Problem habe ich die Tag-Validierung angepasst. Tags werden jetzt mit .strip() bereinigt, mit .lower() klein geschrieben und doppelte Tags werden entfernt.

Für die Datumsfilter habe ich den Fehlerfall angepasst, damit ungültige Datumswerte mit Status Code `422` beantwortet werden.

Bei /notes/stats habe ich die Berechnung der einzigartigen Tags angepasst, damit sie zur /tags-Liste passt.

Nach jeder Änderung habe ich die Tests wieder ausgeführt. Am Ende hat die komplette Test-Suite funktioniert
---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?
Heute habe ich ein einfaches Frontend mit Streamlit für meine Notes API erstellt.

Das Frontend kann die Notes aus meiner API laden und anzeigen. Es zeigt den Titel, den Inhalt, die Kategorie und die Tags einer Note an.

Außerdem habe ich ein Formular eingebaut, mit dem man eine neue Note erstellen kann. Die neue Note wird dann an meine FastAPI API geschickt und in der Datenbank gespeichert.
---

#### 2. 🚧 What challenges did I face?
Ein konkretes Problem war, dass sehr viele alte Testdaten in meiner Datenbank waren. Dadurch wurden im Frontend zu viele Notes angezeigt und die Seite war unübersichtlich.

Außerdem musste ich darauf achten, dass die Tags aus dem Formular richtig an die API geschickt werden. Die Tags werden im Frontend als Text eingegeben, zum Beispiel "urgent, meeting", aber die API erwartet eine Liste von Tags.
---

#### 3. 💡 How did I overcome them?
einfach nochmal das korrigiert. :)
---

### Day 8

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 9

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---


# 🎉 Congratulations! You did it! 🎓✨













