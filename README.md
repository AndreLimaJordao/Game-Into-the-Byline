# Into the Byline
## Equipe 10:
- André Lima Jordão (alj);
- Diego Juan Ferreira da Silva (djfs);
- Eliseu Cordeiro de Brito (ecb2);
- Pedro Inácio Alves dos Santos (pias);
- Rodrigo Florenço dos Santos (rfs6).
---
## Instruções de como rodar o projeto:
    O arquivo python principal é o main.py, só basta rodar ele para iniciar o jogo, detalhe, as seguintes bibliotecas são exigidas: pygame, random, pyamaze e MoviePy.
    Depois que inicializar o jogo, você se encontrará na tela inicial: 
        1. Se apertar a tecla número 1 do seu teclado, você irá iniciar o jogo;
        2. Caso aperte a tecla 2, entrará na página de tutorial;
        3. Se apertar a tecla 3, fechará o jogo.
    Obs.: A tecla "esc" fecha o jogo ao longo de toda a jogatina.
---
## Arquitetura do projeto:
- Interface 2D de vista superior;
- Mapa:
    - Labirinto fechado (sem porta de entrada e saída nas bordas) 20x20;
    - Labirinto gerado aleatoriamente a cada nova jogatina;
    - Baús também gerados aleatoriamente a cada nova jogatina;
    - Contém 20 baús em posições aleatórias possuindo ou não itens;
    - O labirinto só possui uma saída.
- Jogabilidade:
    - Movimentação do player em eixos cartesianos usando o _WASD_;
    - Geração do _flash_ sob eixos cartesianos usando as teclas direcionais;
    - Interação com os baús através do _space_;
    - Uso dos itens pelas seguintes teclas numéricas:
        - Tecla 1: _Glowstick_;
        - Tecla 2: _Radar_;
        - Tecla 3: _Super Battery_.
- Mecânicas:
    - Os monstros (Billy e Bob) se deslocam pelo labirinto da mesma forma que o player e seguindo a rota mais curta entre sua posição e o _player_:
        - Billy Billingham: Se desloca 5 "casas" em direção ao _player_ a cada _flash_ dado;
        - Bob Burningham: Se desloca 3 "casas" em direção ao _player_ a cada _flash_ e 7 "casas" quando abre o baú.
    - O _player_ perde quando um dos mosntros colide com ele, zerando a sua pontuação e finalizando o jogo;
    - O _flash_ expõe todas as casas conseguintes ao sentido da seta pressionada até encontrar uma parede no mesmo sentido, além de ser o único meio com que o _player_ interaja com os baús, visualize os monstros e a porta de saída;
    - Itens:
        - _Key_: Permite que o _player_ consiga escapar do labirinto assim que, no mínimo, 3 _keys_ (do total de 5 distribuídas pelo labirinto) forem coletadas;
        - _Glowstick_: Expõe todas as casas ao redor tanto verticalmente e horizontalmente quanto diagonalmente (em uma área 3x3 em relação ao player);
        - _Radar_: Destaca o posicionamento dos mosntros em coloração laranja até o próximo _flash_ ser disparado;
        - _Super Battery_: Ao ser ativado, o _flash_ irá percorrer ao menos uma parede após ela ter encontrado a primeira (isso se a primeira parede encontrada não for da borda do labirinto), tendo 25% de probabilidade de o disparo do _flash_ seguir até a borda do labirinto (_super duper battery_).
    - Assim que o _player_ coletar 3 _keys_, aparecerá momentaneamente uma indicação da porta de saída no labirinto.
### Função de cada arquivo:
    - main.py: Arquivo principal, onde o jogo realmente irá rodar;
    - boxes.py: Módulo que lida com os baús, desde sua geração até os itens que irá conter;
    - flash.py: Módulo que lida com o flash do player e tudo relacionado com iluminação de rotas e revelação do labirinto;
    - inventory.py: Módulo responsável por tratar do inventário do player;
    - maze_generator.py: Módulo que gera e trata do labirinto;
    - monster.py: Módulo que controla os monstros, tanto o Billy quanto o Bob;
    - player.py: Módulo que instancia o player e suas mecãnicas;
    - score.py: Módulo que controla e manipula a pontuação do player;
    - solve_path: Módulo de uma única função que resolve a rota mais rápida entre 2 pontos;
    - utils: Módulo de funções uilitárias e repetitivas ao longo dos outros módulos.
---
## Concept arts e capturas de tela:
- Concept arts:

- Capturas de tela:
  ![home_screen](https://github.com/user-attachments/assets/8e9b7617-b303-4e6e-8b7a-255733a4f397)
  
  ![guide](https://github.com/user-attachments/assets/5bf5b86c-abde-4170-8520-a1fddcb4402d)
  
  ![Captura de tela 2024-08-03 200210](https://github.com/user-attachments/assets/9dae278b-0949-4a0e-83f1-660a67da8a3c)
  
  ![Captura de tela 2024-08-03 200405](https://github.com/user-attachments/assets/5a9a751a-7b8c-4d0a-acab-01982583fd12)
  
---
## Ferramentas e bibliotecas:
- Ferramentas:
    - Trello: Usada para guiar sobre a evolução e as priopridades das etapas de desenvolvimento do jogo, além de facilitar a comunicação das atualizações no github;
    - Github: Usada para transmitir as versões do jogo para os colaboradores (os permitindo ter contato sempre com a versão mais atual) e controlar/salvar as versões;
    - JetBrains Code With Me: Usada para programação em conjunto durante reuniões;
    - WhatsApp: Usada para comunicação informal;
    - Discord: Usada para comunicação formal e para reuniões;
    - Google Drive: Tranferência de arquivos, como imagens, cutscenes e áudios.
- Bibliotecas:
    - Internas:
        - Random: Escolher p-aleatoriamente valores dentro de intervalos e listas, usada especialmente para gerar a posição do player, dos monstros, dos baús e da porta, definir os itens contidos nos baús e buscar a possibilidade de ativar a _super duper battery_.
    - Externas:
        - Pygame: Biblioteca principal do jogo, usada para gerar a exibição do jogo, efeitos sonoros e dar forma ao player, aos monstros, às caixas e à porta;
        - Pyamaze: Usada para gerar e personalizar o formato do labirinto;
        - MoviePy: Usada exclusivamente para a cutscene de fim de jogo na consição de vitória.

---
## Divisão do trabalho:
- 1ª semana:
    - André Jordão: _Sound design_, _game design_, estudo de algoritmos de solução de labirintos e desenvolvimento da "IA" do monstro;
    - Diego Silva: 
    - Eliseu Brito: _Background design_, _sprite design_, _sound design_, registro para o relatório;
    - Pedro Santos: Gerador de labirintos, exibição do labirinto
    - Rodrigo Santos: Mecânica do _player_ e do _flash_, e interação entre ambos e o labirinto.
- 2ª semana:
    - André Jordão: Aperfeiçoamento da IA do mosntro,  _game design_, _sound design_, tratamento de itens, mecânica de vitória/perda e testes;
    - Diego Silva: 
    - Eliseu Brito: _Background design_, _sprite design_, _sound design_, registro para o relatório;
    - Pedro Santos:
    - Rodrigo Santos: .
---
## Conceitos aproveitados da disciplina:
- Dicionários:
    - Armazenar a situação de cada "casa" do labirinto, delimitar os espaços com ou sem paredes e controlar, manipular e guiar os objetos pelo labirinto;
    - Salvar a rota otimizada de cada monstro;
    - Guardar cada valor de deslocamento do _player_;
    - Associar as abreviações dos itens aos itens propriamente ditos;
    - Registrar o inventário do _player_;
    - Computar o máximo a ser percorrido pelo disparo do _flash_.
- Listas:
    - Reunir as coordenadas dos _flashs_;
    - Armazenar a situação de se um monstro foi pego por um _flash_;
    - Salvar as coordenadas dos baús;
    - Registrar as coordenadas dos _glowsticks_;
    - Guardar as coordenadas dos monstros se o radar for ativado.
- Tuplas:
    - Tudo relacionado a coordenadas, dimensões, resolução e cores.
- Condicionais:
    - Tudo relacionado à comparação de valores ao longo de todo o código;
    - Relacionar as posições do _player_ e do _flash_ com outros objetos, como monstros, baús e porta;
    - Comparar em qual cenário de jogo está o _player_, como menu inicial, jogo em si e cenário de morte/vitória.
 - Loops:
    - Laço principal do jogo;
    - Loop para a captura de eventos;
    - Algoritmo para calcular a rota mais otimizada de cada monstro;
    - Lógica para distribuir os itens nos baús;
    - Loop para caminhar entre listas de tuplas e gerar as paredes necessárias do labirinto na tela.
 - Funções:
    - Códigos utilitários que facilitam a construção do jogo e a exposição de cada objeto na tela.
 - POO:
    - _Player_;
    - _Flash_;
    - Monstros;
    - Inventário;
    - Especiais;
    - Modularização.
---
## Questionamentos do projeto:
1. Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?
2. Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?
3. Quais as lições aprendidas durante o projeto?
