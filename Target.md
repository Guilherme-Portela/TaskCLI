## 🚀 PROJETO 1 — “Gerenciador de Tarefas CLI — Versão Arkan 0.1”

Um clássico… mas com tempero de disciplina e honra do tatame.

## 🎯 Objetivo

Criar um gerenciador de tarefas em linha de comando, que funcione totalmente offline, usando apenas o terminal.
Nada de interface gráfica. Nada de requisições externas.

A ideia é treinar:

* manipulação de arquivos

* entrada e saída no terminal

* erros previsíveis e imprevistos

* design de código mínimo, limpo e robusto

* começo de organização modular

## 🧱 Especificação Técnica (Requisitos obrigatórios)
### 📌 1. O programa deve ter estes comandos principais:

```add <texto da tarefa>```

``list``

``remove <id>``

``done <id>``

``clear (remove todas as tarefas com confirmação)``

| Nota: IDs devem ser gerados automaticamente.

### 📌 2. Armazenamento dos dados

Um arquivo local tasks.db ou tasks.json, escolha sua.

Se o arquivo não existir, o programa cria.

Se estiver corrompido, o programa não deve crashar → deve criar outro arquivo de forma segura.

### 📌 3. Tratamento de erros obrigatório

Você deve prever e lidar com:

``Comando inválido`

``ID inexistente``

``Falta de argumento``

``Falha de leitura/gravação em disco``

``Arquivo inexistente``

``Arquivo corrompido``

``Permissão negada (dependendo do SO)``

``Execução sem argumentos``

Cada erro deve ter mensagens claras e humanas, não monstrinhos técnicos.

📌 4. Requisitos de robustez

* Código modular (sem jogar tudo no mesmo arquivo gigante)

* Funções separadas por responsabilidade

* Nada de variáveis globais desnecessárias

* Log simples opcional (arquivo log.txt)

### 📌 5. Requisitos de segurança (básico por enquanto)

* Não permitir path traversal

* Não permitir sobrescrever arquivos aleatórios

* Validar entrada do usuário para evitar comando malformado

### 📌 6. Experiência de uso

* O programa deve ser amigável no terminal:

* mensagens claras

* organização

* feedback visual simples (✔, ✖, etc. — opcional)

### 🎒 Regras do aprendizado

**Você pode usar APENAS**:

* documentação oficial da linguagem

* documentação de bibliotecas nativas

* blogs técnicos e relatos de engenheiros

* stackoverflow somente lendo perguntas/erros (não soluções)

**Você NÃO pode**:

* pedir código

* copiar código

* usar ferramentas que geram implementação pronta

* pedir dicas “como implementar X”

Eu sou só o mestre-velho que aponta a lua. Você constrói a nave.