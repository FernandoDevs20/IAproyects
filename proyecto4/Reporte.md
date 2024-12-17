# **Proyecto: Análisis de la Reforma al Poder Judicial y a los Organismos Autónomos en México**

# Alumno: Fernando Rodriguez Gonzalez

## **Descripción General**
Este proyecto tiene como objetivo **extraer, procesar y analizar información crítica** relacionada con la **Reforma al Poder Judicial** y la **Reforma a los Organismos Autónomos en México**.  
Se utilizaron herramientas tecnológicas modernas para responder **preguntas específicas** sobre estos temas de manera fundamentada y sin especulaciones.

---

## **Justificación del Enfoque**

La información fue recopilada de **tres tipos de fuentes principales**:

### **1. Documentos PDF (Análisis Objetivo y Estructurado)**
- Proveen información **técnica, formal y objetiva**, libre de opiniones personales.
- Estos documentos suelen ser estudios oficiales o propuestas gubernamentales.
- **Ventaja principal:** Permiten entender los **fundamentos legales y técnicos** de las reformas sin interferencias.

### **2. Páginas Web (Contexto, Opiniones y Consecuencias)**
- Los artículos de noticias y reportajes ofrecen:
   - **Contexto histórico y actual** de las reformas.
   - **Opiniones de expertos** y posibles impactos sociales.
   - **Consecuencias inmediatas** percibidas en la opinión pública.
- **Ventaja principal:** Complementan la información técnica con una visión **más contextual y crítica**.

### **3. Reddit (Descartado)**
- Las publicaciones en Reddit fueron evaluadas inicialmente, pero descartadas debido a:
   - La **falta de contenido relevante** y específico sobre las reformas.
   - La predominancia de **opiniones subjetivas** y no verificadas.
- **Decisión final:** Se priorizaron fuentes **estructuradas y verificables**.

---

## **Fases del Proyecto**

### **1. Búsqueda y Selección de Información**
Se recopilaron enlaces relevantes de:  
- **Páginas web oficiales y de noticias**.  
- **Archivos PDF con contenido técnico y formal**.

---

### **2. Extracción de Información (Web Scraping)**

#### **a) Extracción de Páginas Web Dinámicas**  
- **Herramienta:** Selenium  
- **Método:** Automatización de un navegador Chrome para extraer contenido dinámico (etiquetas `<p>` y encabezados `<h2>`, `<h3>`).

```python
def process_dynamic_links():
    with open(ORGANISMOSAUTONOMOS, "a", encoding="utf-8") as combined_file:
        combined_file.write("### Contenido Dinámico ###\n")
        for link in dynamic_links:
            try:
                driver.get(link)  # Abre el enlace
                title = driver.title  # Captura el título de la página
                
                # Captura encabezados H2, H3 y párrafos
                headers_h2 = driver.find_elements(By.TAG_NAME, "h2")
                headers_h3 = driver.find_elements(By.TAG_NAME, "h3")
                paragraphs = driver.find_elements(By.TAG_NAME, "p")
                
                # Escribe el título de la página
                combined_file.write(f"Título: {title}\n")
                
                # Escribe encabezados H2
                combined_file.write("Encabezados H2:\n")
                combined_file.write("\n".join([h2.text for h2 in headers_h2 if h2.text.strip()]) + "\n\n")
                
                # Escribe encabezados H3
                combined_file.write("Encabezados H3:\n")
                combined_file.write("\n".join([h3.text for h3 in headers_h3 if h3.text.strip()]) + "\n\n")
                
                # Escribe párrafos
                combined_file.write("Contenido:\n")
                combined_file.write("\n".join([p.text for p in paragraphs if p.text.strip()]) + "\n\n")
            
            except Exception as e:
                print(f"Error procesando {link}: {e}")
```

---

#### **b) Extracción de Contenido de PDFs**  
- **Herramienta:** PDFPlumber  
- **Método:** Extracción del texto de cada página de los PDFs descargados.

```python
def process_pdf_links():
    with open(ORGANISMOSAUTONOMOS, "a", encoding="utf-8") as combined_file:
        combined_file.write("### Contenido de PDFs ###\n")
        for link in pdf_links:
            try:
                response = requests.get(link, verify=False)
                pdf_path = "temp.pdf"
                with open(pdf_path, "wb") as file:
                    file.write(response.content)
                with pdfplumber.open(pdf_path) as pdf:
                    content = "".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                combined_file.write("Contenido:\n")
                combined_file.write(content + "\n\n")
            except Exception as e:
                print(f"Error procesando {link}: {e}")
```

---

### **3. Consolidación de Información**  
Toda la información fue unificada en un archivo de texto:  

- **`contenido_PODERJUDICIAL.txt`**

Esto solo par el poder judicial ya que se hizo otro con otros links para poder hacer el analisis de la ley a los organismos autonomos
---

### **4. Preparación del Modelo de Lenguaje**

#### **Herramientas Utilizadas:**
1. **Ollama:**  
   - **Manejador de modelos de lenguaje** que permite ejecutar **Llama 3.2** de manera local.  
2. **AnythingLLM:**  
   - Permite cargar el archivo txt, para generar **vectores semánticos** y realizar búsquedas rápidas y precisas, por lo que entiendo es poner en términos matemáticos el texto que le estamos pasando para que pueda hacer búsquedas más efectivas.

#### **Proceso:**
Subir el archivo es de los más sencillo que se puede hacer ya que solo a nuestro espacio de trabajo en donde previamente le decimos que trabaje con llama 3.2 tiene una opción de subir archivos, se suben a una carpeta y después se pasan al espacio de trabajo que pueda guardarlo generando los vectores, osea poner en términos matemáticos la información que le pasamos.

---

### **5. Creación del Prompt Específico**

Creamos un prompt para que nuestro modelo de lenguaje o inteligencia artificial sepa o tenga una guia de qué es lo que debe de hacer, además de especificar que trabaje con la información que le pasamos previamente, le asignamos un rol y posibles formas de contestar a las preguntas, como si queremos que nos de resumido que no es nuestro caso:

```text
Responde de manera precisa, detallada y profunda a las preguntas proporcionadas **analizando a fondo el contenido del texto dado**.  
Si no encuentras una respuesta directa, realiza una búsqueda exhaustiva en todo el contenido, conecta ideas entre diferentes secciones y presenta **deducciones fundamentadas** basadas en los fragmentos relevantes.  
Evita respuestas breves o incompletas; tu objetivo es entregar una **respuesta completa** que explique el contexto, la información exacta encontrada y su posible relación con la pregunta.

Formato de respuesta:

Pregunta: [Reescribe la pregunta aquí].  
Respuesta: [Proporciona una explicación amplia y detallada del tema, conectando fragmentos del texto y realizando análisis cuando sea necesario].  
Deducción (si aplica): ["Explica razonamientos lógicos o inferencias que puedan derivarse del texto, incluso si la información no es explícita"].    
```

---

### **6. Prueba del Modelo**  
Se realizaron preguntas clave para evaluar la precisión del modelo, tales como: 
 Preguntas para la Ley del Poder Judicial
 1. ¿El diagnóstico de la ley al poder judicial es conocido y qué estudios
 expertos se tuvieron en cuenta?

 R: Se menciona que el diagnóstico del estado actual del sistema judicial fue realizado por un análisis individual llevado a cabo por el personal del poder judicial, así como por los panelistas y participantes en talleres.

En este sentido, es necesario considerar que se llevaron a cabo estudios expertos en la materia.

2. ¿Por qué la reforma no incluyó a las fiscalías y a la defensoría, limitán
dose solo al poder judicial?
R: Se menciona que la reforma se centró en el Poder Judicial debido a su mayor impacto en la aplicación de las leyes y su necesidad de protección. Asimismo, se consideró implementar un mecanismo de denuncia y seguimiento para identificar y combatir a los grupos armados.

En este contexto, se puede deducir que el poder judicial fue el foco principal debido a su mayor presencia en la aplicación de las leyes.

3. ¿Qué medidas concretas se implementarán para evitar la captación del
R:Se menciona que es necesario tomar medidas para evitar la captación del crimen organizado y la violencia en el contexto electoral. En este sentido, se pueden implementar las siguientes medidas:

Se deben establecer mecanismos de denuncia y seguimiento para identificar y combatir a los grupos armados.
Se debe fortalecer la seguridad física y operacional en los centros de votación y otros lugares estratégicos, así como en el transporte de votantes.

 crimen organizado y la violencia en el contexto electoral?

4. ¿Cómo garantizar que juristas probos y honestos se animen a competir públicamente frente a los riesgos de la violencia?
R: Para garantizar que juristas probos y honestos se animen a competir públicamente frente a los riesgos de la violencia, se podrían implementar las siguientes medidas:

Crear un entorno seguro: Establecer canales de comunicación seguros y anónimos para que los juristas puedan expresarse sin miedo a represalias.
Fomentar el diálogo: Organizar debates, seminarios y jornadas donde se discutan las propuestas y sus impactos, permitiendo a los juristas intercambiar ideas de manera constructiva.
Promover la transparencia: Facilitar acceso a información sobre las reformas y sus procesos de toma de decisiones, para que los juristas puedan evaluarlas de manera objetiva.
Establecer mecanismos de denuncia: Crear un sistema de denuncia y seguimiento para identificar y abordar cualquier incidente de violencia o represalia contra los juristas.
Reconocer y recompensar el trabajo: Reconocer y recompensar al jurisdicción por su dedicación al servicio público, lo que puede motivarlo a seguir trabajando en reformas importantes.

5. ¿Cómo se conforman los comités de postulación?  
R: Según el contexto proporcionado:

“Los Comités de Evaluación publicarán, dentro de los 15 días naturales posteriores a su integración, las convocatorias para participar en el proceso de evaluación y selección de postulaciones, para la elección de personas juzgadoras.”

No se menciona explícitamente cómo están conformados los comités de evaluación. Sin embargo, se puede inferir que serán formados por una o más personas designadas específicamente para este fin, pero no se proporciona información adicional sobre su composición o estructura organizativa.

6. ¿Cómo asegurar la carrera judicial?
R: Para asegurar la carrera judicial se pueden implementar las siguientes medidas:

Establecer un sistema de evaluación y selección transparente: Crear un proceso que evalúe y seleccione a los candidatos para el cargo de juez o magistrado, basándose en criterios objetivos y no políticos.
Fomentar la diversidad e inclusión: Asegurar que las jurisdicciones sean representativas de la sociedad, con una amplia variedad de perfiles y perspectivas.
Proporcionar capacitación y desarrollo profesional: Ofrecer oportunidades de capacitación y desarrollo profesional para los funcionarios judiciales, para que puedan mantenerse actualizados en las últimas tendencias y tecnologías.
Establecer un sistema de supervisión y control: Crear un mecanismo de supervisión y control que garantice la transparencia y rendición de cuentas en el funcionamiento del poder judicial.
Promover la integridad y ética profesional: Fomentar una cultura de integridad y ética profesional en las jurisdicciones, mediante programas de sensibilización y concienciación sobre la importancia de la conducta ética.

 7. ¿Cómo compatibilizar la incorporación de medidas para preservar laidentidad de los jueces (conocidos en el sistema interamericano como"jueces sin rostro") con los estándares internacionales?
R: Se menciona que la Corte IDH ha tenido la oportunidad de analizar la figura de los «jueces sin rostro» en diversos casos conocidos contra Perú. Esto trajo como consecuencia la construcción de una sólida línea jurisprudencial en donde se considera que los juicios ante jueces “sin rostro” o de identidad reservada infringen el artículo 8.1 de la Convención Americana, «pues impide a los procesados conocer la identidad de los juzgadores y por ende valorar su idoneidad y competencia, así como determinar si se configuraban causales de recusación, de manera de poder ejercer su defensa ante un tribunal independiente e imparcial«.

En este contexto, se puede inferir que la incorporación de medidas para preservar la identidad de los jueces es compatible con los estándares internacionales, pero requiere una implementación cuidadosa y respetuosa de las normas y principios establecidos en la Convención Americana.

Por lo tanto, se puede decir que:

La Corte IDH ha establecido una línea jurisprudencial clara sobre los juicios ante jueces “sin rostro” y sus implicaciones para el derecho a un juicio justo.
La incorporación de medidas para preservar la identidad de los jueces es compatible con los estándares internacionales, pero requiere una implementación cuidadosa y respetuosa de las normas y principios establecidos en la Convención Americana.

8. ¿Cómo impactará el costo económico de esta reforma en la promoción
 y el acceso a la justicia?

R: El costo económico de la reforma puede tener un impacto significativo en la promoción y el acceso a la justicia.

Posibles consecuencias del aumento del costo:

Limitación del acceso: El aumento del costo podría llevar a que una mayor proporción de personas no puedan acceder a los servicios judiciales debido a su incapacidad económica para pagarlos.
Desigualdad en la justicia: La reforma podría exacerbar las desigualdades existentes en el sistema judicial, ya que aquellos con más recursos podrían tener mayor acceso a los servicios y recursos disponibles.
Posibles consecuencias del mantenimiento de un costo estable:

Estabilidad y seguridad: Mantener un costo estable podría asegurar la estabilidad y seguridad en el sistema judicial, lo que permitiría una mayor confianza entre las partes involucradas.
Mayor eficiencia: Un costo estable podría fomentar una mayor eficiencia en el sistema judicial, ya que los funcionarios judiciales podrían enfocarse en proporcionar servicios de alta calidad sin la presión de un aumento constante de costos.
Posibles soluciones:

Subvenciones y financiamiento público: El gobierno podría considerar subvenciones o financiamiento público para ayudar a cubrir los costos del sistema judicial.
Innovación y eficiencia: La implementación de tecnologías y prácticas innovadoras podría ayudar a reducir los costos sin comprometer la calidad de los servicios.
Negociaciones con partes interesadas: Es posible que las partes interesadas, como las empresas o organizaciones, puedan acordar contribuir a los costos del sistema judicial como parte de sus obligaciones sociales o legales.

## Preguntas para la Ley de Organismos Autónomos

1. ¿Esconstitucional esta ley, considerando que algunos organismos autónomos están establecidos en la Constitución?
R:  Análisis constitucional:

Definición constitucional de los organismos autónomos: Según el artículo 115 de la Constitución, los organismos autónomos son “establecidos por ley federal o local” y tienen “competencias específicas”.
Enfoque en la legalidad y competencia: Establece que los organismos autónomos están sujetos a la Constitución, la ley federal y la ley local, lo cual garantiza su legitimidad y limita su poder.
Reconocimiento constitucional del principio de autonomía: La POA reconoce el principio de autonomía en las instituciones públicas y establece mecanismos para que las instituciones autónomas ejercen sus funciones de manera efectiva y responsable.
Posibles argumentos a favor de la Constitucionalidad:

La POA ofrece un marco legal claro y seguro para los organismos autónomos, garantizando su legitimidad y responsabilidad.
Al establecer mecanismos de supervisión y rendición de cuentas, la POA protege el principio de autonomía y asegura que las instituciones públicas funcionen de manera eficiente y transparente.

2. ¿Cómo afectaría la eliminación de estos organismos a la transparencia y rendición de cuentas del gobierno?
R: Efectos en la transparencia:

Falta de supervisión: La eliminación de los OCA podría llevar a una falta de supervisión sobre el uso de fondos públicos, lo que dificultaría la transparencia en la gestión gubernamental.
Limitación de la información pública: La ausencia de un órgano de control independiente podría limitar la disponibilidad de información pública sobre las actividades y decisiones del gobierno.
Efectos en la rendición de cuentas:

Pérdida de mecanismos de control: La eliminación de los OCA podría llevar a una pérdida de mecanismos de control que garantizan la rendición de cuentas del gobierno.
Disminución de la confianza pública: La falta de transparencia y control sobre el uso de fondos públicos podría disminuir la confianza pública en el gobierno.
Riesgos adicionales:

Abuso de poder: La ausencia de un órgano de control independiente podría generar un entorno propicio para el abuso de poder por parte de los funcionarios gubernamentales.
Ineficiencia y corrupción: La falta de supervisión y rendición de cuentas podría llevar a una mayor probabilidad de ineficiencia y corrupción en la gestión pública.
Posibles consecuencias:

Pérdida de legitimidad del gobierno: La falta de transparencia y control sobre el uso de fondos públicos podría llevar a una pérdida de legitimidad del gobierno.
Disminución de la confianza pública: La ausencia de mecanismos de control y supervisión podría disminuir la confianza pública en el gobierno.

3. ¿Quéfunciones críticas podrían perder independencia y control al pasar al poder ejecutivo u otras instituciones?
R: Funciones críticas que podrían perder independencia y control:

El Poder Judicial: La eliminación de los OCA podría afectar la independencia del Poder Judicial, ya que estos organismos proporcionan un control externo sobre las decisiones judiciales y garantizan la integridad de la justicia.
La Comisión Nacional de Defensa (CND): La CND es responsable de supervisar y regular el ejército, lo que podría verse afectado si los OCA pierden independencia y control.
El Instituto Federal de Acceso a la Información Pública (INAI): El INAI se encarga de garantizar la transparencia y rendición de cuentas en las instituciones gubernamentales, lo que podría verse afectado si los OCA pierden independencia y control.
El Instituto Nacional Electoral (INE): El INE es responsable de supervisar las elecciones y garantizar la integridad del proceso democrático, lo que podría verse afectado si los OCA pierden independencia y control.
La Comisión de Transparencia y Acceso a la Información Pública (COTAPI): La COTAPI se encarga de promover la transparencia y rendición de cuentas en las instituciones gubernamentales, lo que podría verse afectado si los OCA pierden independencia y control.
El Consejo Nacional de Transparencia (CONAT): El CONAT es responsable de supervisar la implementación de políticas de transparencia y rendición de cuentas en las instituciones gubernamentales, lo que podría verse afectado si los OCA pierden independencia y control.
El Instituto Federal de Comercio (IFCE): El IFCE es responsable de supervisar la industria y garantizar la integridad del mercado, lo que podría verse afectado si los OCA pierden independencia y control.
Posibles consecuencias:

Pérdida de confianza en las instituciones: La falta de independencia y control de estas instituciones podría llevar a una pérdida de confianza en ellas por parte del público.
Ineficiencia y corrupción: La ausencia de mecanismos de control y supervisión podría llevar a una mayor probabilidad de ineficiencia y corrupción en las instituciones.
Disminución de la transparencia y rendición de cuentas: La falta de independencia y control de estas instituciones podría dificultar la transparencia y rendición de cuentas en las instituciones gubernamentales.
Posibles alternativas:

Reformas institucionales: Se podrían implementar reformas institucionales para fortalecer la independencia y control de estas instituciones.
Creación de nuevos organismos: Podría considerarse la creación de nuevos organismos autónomos o mecanismos de control para compensar la ausencia de los OCA.
Importancia:

La independencia y el control de las instituciones son fundamentales para garantizar la transparencia y rendición de cuentas en las instituciones gubernamentales.
La pérdida de confianza en estas instituciones podría tener graves consecuencias para la democracia y la gobernanza en México.

4. ¿Existen alternativas para mejorar la eficiencia de los organismos autónomos sin eliminarlos?
R: Alternativas para mejorar la eficiencia de los organismos autónomos:

Reforma administrativa: Se debería implementar una reforma administrativa que simplifique y reduzca la burocracia en las instituciones.
Descentralización: La descentralización puede ayudar a mejorar la eficiencia al permitir que los organismos autónomos tomen decisiones más rápido y de manera más efectiva.
Implementación de tecnologías: Implementar tecnologías, como sistemas de gestión de información, pueden ayudar a mejorar la eficiencia y la transparencia en las instituciones.
Capacitación y formación: Se debería brindar capacitación y formación a los miembros del personal de las instituciones para mejorar sus habilidades y competencias.
Ejemplos de reformas exitosas:

Reforma en el gobierno federal mexicano: En 2014, México implementó una serie de reformas administrativas que incluyeron la creación de un sistema de gestión de información más eficiente y la descentralización de algunas funciones.
Reforma en Argentina: Argentina también implementó una serie de reformas administrativas en el 2015, incluyendo la creación de un comité de transparencia y rendición de cuentas para mejorar la eficiencia y la transparencia en las instituciones.

5. ¿Quésectores de la sociedad civil y grupos de interés se verían afectados por la desaparición de estos organismos?
R: Sectores de la sociedad civil y grupos de interés que podrían verse afectados:

Organizaciones no gubernamentales (ONGs): Las ONGs dependen en gran medida de los organismos autónomos para recibir financiamiento, recursos humanos y apoyo técnico.
Comunidades locales: Las comunidades locales pueden depender de los organismos autónomos para acceder a servicios básicos como la atención médica, la educación y el agua potable.
Grupos de derechos humanos: Los grupos de derechos humanos dependen de los organismos autónomos para recopilar información y testimonios sobre violaciones de derechos humanos.
Empresarios y productores rurales: Los empresarios y productores rurales pueden depender de los organismos autónomos para acceder a recursos y apoyo técnico.
Impacto en la sociedad:

Pérdida de acceso a servicios básicos: La desaparición de los organismos autónomos podría llevar a una pérdida de acceso a servicios básicos como la atención médica, la educación y el agua potable.
Disminución de la participación ciudadana: La desaparición de los organismos autónomos podría disminuir la participación ciudadana en la toma de decisiones políticas y sociales.
Aumento de la corrupción: La falta de regulación y supervisión podría llevar a un aumento de la corrupción en el sector público.
Alternativas para mitigar los impactos:

Reestructuración de las instituciones: Se debería considerar reestructurar las instituciones para asegurar que sigan cumpliendo con sus funciones esenciales.
Creación de nuevos organismos: Se podrían crear nuevos organismos para reemplazar a los desaparecidos, con la misma misión y objetivo.
Fomento de la participación ciudadana: Se debería fomentar la participación ciudadana en la toma de decisiones políticas y sociales para asegurar que las instituciones se ajusten a las necesidades de la sociedad.
---

## **Tecnologías y Herramientas Utilizadas**

1. **Lenguaje de Programación:**  
   - Python  

2. **Librerías y Frameworks:**  
   - Selenium: Automatización del navegador.  
   - PDFPlumber: Extracción de texto de PDFs.  
   - Requests: Descarga de contenido web.  
   - PRAW: Extracción inicial de Reddit (descartado).  

3. **Manejador de Modelos de Lenguaje:**  
   - Ollama (Modelo Llama 3.2).  

4. **Gestión de Contenido y Vectores:**  
   - AnythingLLM.

---

## Mis conclusiones

# Reforma al poder judicial
Creo que es una reforma que sí viene a cambiar algo que tal vez sí debía cambiar. Hablando sobre su aspecto más importante, creo yo que es la elección de los jueces por voto popular, ya que en otros países sí se eligen a los jueces de esta manera. Pero creo que la forma en la que se está haciendo es el aspecto controversial de esta reforma, ya que los candidatos a estos puestos van a ser elegidos por los diferentes poderes de la nación.

El hecho de dejar esto todavía en manos del mismo gobierno me parece que puede generar un desbalance en el poder, ya que un pequeño grupo de personas podría poner a los candidatos que ellos quieran o los que más les convengan. Además, el aspecto económico también puede tener un impacto en el acceso a la justicia, lo cual sí podría ser demasiado grave.

En un análisis más general, creo que el gobierno actual solo quiere acumular más y más poder, quitando todos los obstáculos en el medio. El Poder Judicial ha sido un problema a la hora de implementar nuevas reformas, como la de los organismos autónomos.

En conclusión, puedo decir que estoy en contra, ya que aunque sí es algo que se debería implementar, no se está implementando de la mejor manera. Además, ciertas acciones nos hacen pensar que hay intenciones ocultas detrás de esta reforma.

## Ley de organismos autónomos

Creo que en esta ley, desde un principio, puedo decir que estoy rotundamente en contra, ya que, imaginándome que soy un trabajador, es ilógico pensar que yo mismo me puedo supervisar. Además, instituciones como el IFT o la COFECE son importantísimas, ya que regulan y se aseguran de que empresas, como las de telecomunicaciones (por ejemplo, Telcel), no abusen de los consumidores. La COFECE es esencial para garantizar que las empresas compitan entre sí de manera justa.

Ahora, la gente no tiene una confianza total en el gobierno, por lo cual eliminar organismos que vigilen y supervisen al mismo gobierno genera bastante desconfianza. Por ejemplo, el INAI nos garantizaba nuestro derecho a la información y la transparencia. En varias ocasiones, este organismo destapó casos de corrupción, y ahora que no está, es peligroso que no podamos acceder a datos importantes sobre cómo se está utilizando el dinero de los impuestos.

Por ejemplo, necesitamos conocer la inversión en proyectos como el Tren Maya o la refinería de Dos Bocas.

En conclusión, estoy totalmente en contra de esta ley. Necesitamos organismos imparciales que protejan a la sociedad. Además, el objetivo que quieren lograr, que es evitar la redundancia de organismos y ahorrar presupuesto, se puede alcanzar con otras estrategias que no desprotejan a la sociedad.

Por último, creo que esta ley representa otro intento más de acumular poder.


