#include <DHT.h>

// Nivel de P --> botao azul
// Nivel de K --> botao amarelo
// Nivel de pH --> LDR
// Umidade --> DHT22
// Relé --> bomba irrigação


#define buttonPin_P 18  // Pino button nivel P
#define pinLED_bt_P 19  // Pino led nivel P
#define buttonPin_K 22  // Pino button nivel k
#define pinLED_bt_K 21  // Pino led nivel k
#define pinLDR_PH 34     // Pino LDR Nivel pH
#define pinoDHT 23     // Pino DHT22
#define modelo DHT22
#define pinRele_irr 4 // Pino bomba de irrigação



DHT dht(pinoDHT, modelo);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(buttonPin_P, INPUT_PULLUP); 
  pinMode(pinLED_bt_P, OUTPUT); 
  pinMode(buttonPin_K, INPUT_PULLUP); 
  pinMode(pinLED_bt_K, OUTPUT); 
  pinMode(pinRele_irr, OUTPUT);
}

void loop() {
   int time_irrig;// Variável para o tempo de irrigação em milissegundos


  // Leitura do botao azul( sensor nivel P)****************
  int buttonState_P = digitalRead(buttonPin_P); // Lê o estado do botão
  bool nivel_P = true;

  Serial.println("");
    if (buttonState_P == LOW) {  // O botão está pressionado (pino conectado ao GND)
        digitalWrite(pinLED_bt_P, HIGH);  // Liga o LED AZUL
        nivel_P = true;
        Serial.println("Nivel de Fosforo (P): NORMAL");
    } else {  // O botão não está pressionado (pino em estado HIGH)
        digitalWrite(pinLED_bt_P, LOW);   // Desliga o LED AZUL
        nivel_P = false;
        Serial.println("Nivel de Fosforo (P): INSUFICIENTE");
    }
    delay(50);  // Pequeno atraso para evitar ruído de contato (debounce)


  
  // Leitura do botao verde( sensor nivel K)****************
  int buttonState_K = digitalRead(buttonPin_K); // Lê o estado do botão
  bool nivel_K = true;
    if (buttonState_K == LOW) {  // O botão está pressionado (pino conectado ao GND)
        digitalWrite(pinLED_bt_K, HIGH);  // Liga o LED VERDE
        nivel_K = true;
        Serial.println("Nivel de Postassio (K): NORMAL");
    } else {  // O botão não está pressionado (pino em estado HIGH)
        digitalWrite(pinLED_bt_K, LOW);   // Desliga o LED AZUL
        nivel_K = false;
        Serial.println("Nivel de Postassio (K): INSUFICIENTE");
    }
    delay(50);  // Pequeno atraso para evitar ruído de contato (debounce)


  // Leitura do LDR ( sensor de PH)**********************
  int ldrValue_PH = analogRead(pinLDR_PH);
  int ldrScaled_PH = map(ldrValue_PH, 0, 1023, 0, 14); // Mapeia os valores de 0 a 1023 para 0 a 14
  Serial.print("Nível de PH (0-14): ");
  Serial.println(ldrScaled_PH);


  // Leitura do DHT22 ( sensor umidade)
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  if (isnan(h) || isnan(t)) {
    Serial.println("Falha no DHT!");
  } else {
    Serial.print("Umidade: ");
    Serial.print(h);
    Serial.println("% ");
    Serial.print("Temperatura: ");
    Serial.print(t);
    Serial.println("*C");
  }

  // Controle de irrigação com base nos niveis de P, K , Ph e Umidade
  // Considerando os valores ideias para cultura de "BANANA"
   float P = 82.00; // Nivel fosforo (P)
   float K = 50.00; // Nivel de potassio (K)
   int pH = 6; // Nivel de Ph
   float umidade = 80.00; // umidade

  
  if ((nivel_P == false)|| (nivel_K == false)||(ldrScaled_PH < pH)||(h < umidade)) {
    time_irrig = 3000; // Tempo de irrigação mais longo (3 segundos)
    Serial.println("Tempo de irrigação mais longo 3s");
  } else {
    time_irrig = 2000; // Tempo de irrigação moderado (2 segundos)
    Serial.println("Tempo de irrigação moderado 2s");
  }

  // Acionamento da bomba de irrigação
  digitalWrite(pinRele_irr, HIGH); // Liga a bomba
  delay(time_irrig);        // Mantém a bomba ligada pelo tempo determinado
  digitalWrite(pinRele_irr, LOW);  // Desliga a bomba  
 
  delay(4000); // Ajuste o tempo de leitura conforme necessário
}
