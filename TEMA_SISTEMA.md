# Sistema de Temas - Tema Claro e Dark

## 🎨 Funcionalidades de Tema

O sistema agora suporta **tema claro e dark** com alternância automática e persistente.

### ✨ Recursos

- **Tema Claro**: Design padrão com cores Facebook (azul claro)
- **Tema Dark**: Design noturno com cores escuras e indigo
- **Persistência**: O tema escolhido é salvo no navegador
- **Transições Suaves**: Mudanças de tema com animações
- **Botão Flutuante**: Sempre disponível no canto da tela
- **Múltiplas Opções**: Três maneiras diferentes de alternar tema
- **Responsivo**: Funciona em desktop e mobile

### 🎯 Como Usar

#### Dashboard (Novo!)
- Clique no **botão destacado "Tema Claro/Dark"** no topo da página
- Veja o indicador visual mostrando qual tema está ativo
- O tema alterna instantaneamente em toda a página
- A preferência é salva automaticamente

#### Desktop
- Clique no botão **"Tema Claro/Dark"** na sidebar esquerda
- **OU** clique no **botão flutuante** no canto inferior direito
- O ícone alterna entre ☀️ (claro) e 🌙 (dark)
- O tema é salvo automaticamente

#### Mobile
- Abra o menu hambúrguer (☰)
- Clique no botão **"Tema"** no topo
- **OU** clique no **botão flutuante** (sempre visível)
- O tema alterna automaticamente

### 🎨 Paleta de Cores

#### Tema Claro
- **Fundo**: Gradiente azul claro (#f5f7fa → #c3cfe2)
- **Cards**: Branco (#ffffff)
- **Sidebar**: Gradiente azul claro (#e7f3ff → #d1e7ff)
- **Texto Sidebar**: Preto (#000000)
- **Texto**: Preto (#000000) e cinza (#e1e8ed)
- **Azul**: Facebook (#1877f2)

#### Tema Escuro (Dark)
- **Fundo**: Gradiente escuro (#0f0f23 → #1a1a2e)
- **Cards**: Azul muito escuro (#1a1a2e)
- **Sidebar**: Gradiente navy (#16213e → #0f0f23)
- **Texto Sidebar**: Branco (#f1f5f9)
- **Texto**: Branco (#ffffff) e cinza claro (#e2e8f0)
- **Indigo**: Indigo médio (#6366f1) para destaques

### 🔧 Implementação Técnica

#### CSS Variables
```css
:root {
  --bg-primary: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  --text-primary: #50596c;
  --text-blue: #1877f2;
  /* ... mais variáveis */
}

[data-theme="dark"] {
  --bg-primary: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  --text-primary: #e1e8ed;
  --text-blue: #1da1f2;
  /* ... variáveis do tema escuro */
}
```

#### JavaScript
- Detecta tema salvo no `localStorage`
- Alterna atributo `data-theme` no HTML
- Atualiza ícones e textos dos botões
- Salva preferência do usuário

### 📱 Responsividade

- **Desktop**: Botão na sidebar com texto completo
- **Tablet**: Botão na sidebar com texto reduzido
- **Mobile**: Botão no navbar com ícone apenas

### 🎭 Efeitos Visuais

- **Transições**: 0.3s ease para todas as mudanças
- **Hover**: Efeitos nos botões e links
- **Animações**: Fade-in nos elementos
- **Sombras**: Adaptáveis ao tema

### 💾 Persistência

- **localStorage**: Salva preferência do usuário
- **Padrão**: Tema claro se não houver preferência salva
- **Cross-session**: Mantém tema entre sessões

### 🔘 Botão Flutuante

- **Posição**: Fixo no canto inferior direito (30px da borda)
- **Design**: Circular, 60px × 60px (50px em mobile)
- **Ícone**: Sol (☀️) para tema claro, lua (🌙) para tema escuro
- **Animações**: Hover scale (1.1x) e click scale (0.95x)
- **Z-index**: 1050 (acima de outros elementos)
- **Responsivo**: Adapta tamanho em telas menores que 576px

### 🚀 Benefícios

1. **Acessibilidade**: Melhor contraste e legibilidade
2. **UX**: Preferência pessoal do usuário
3. **Moderno**: Design atual com temas dinâmicos
4. **Performance**: CSS variables para mudanças rápidas
5. **Compatibilidade**: Funciona em todos os navegadores modernos

---

**Desenvolvido para o Sistema RH - 2026**</content>
<parameter name="filePath">c:\Users\nando\Downloads\Projeto_Python_RH-master\TEMA_SISTEMA.md