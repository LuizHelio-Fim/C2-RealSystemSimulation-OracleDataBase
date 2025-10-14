// test-debug.js - Funções de teste e diagnóstico

// ===== FUNÇÕES DE TESTE E DIAGNÓSTICO =====

async function testBackendConnection() {
  try {
    console.log('🔄 [TESTE] Testando conexão com backend...');
    showLoading('Testando conexão com backend...');
    
    // Teste 1: Verificar se as funções existem
    console.log('1️⃣ Verificando funções de relatórios...');
    console.log('apiService existe?', typeof apiService !== 'undefined');
    console.log('getCourseStatistics existe?', typeof apiService.getCourseStatistics === 'function');
    console.log('getOffersCompleteReport existe?', typeof apiService.getOffersCompleteReport === 'function');
    
    // Teste 2: Conexão básica
    console.log('2️⃣ Testando endpoint raiz...');
    const connectionTest = await apiService.testConnection();
    console.log('✅ Conexão básica OK:', connectionTest);
    
    // Teste 3: Endpoint de reports
    console.log('3️⃣ Testando endpoint de reports...');
    const reportsTest = await apiService.testReportsEndpoint();
    console.log('✅ Endpoint de reports OK:', reportsTest);
    
    // Teste 4: Tentar chamar as funções específicas
    console.log('4️⃣ Testando chamadas específicas...');
    
    try {
      const courseStats = await apiService.getCourseStatistics();
      console.log('✅ getCourseStatistics funcionou:', courseStats);
    } catch (err) {
      console.log('❌ getCourseStatistics falhou:', err.message);
    }
    
    try {
      const offersReport = await apiService.getOffersCompleteReport();
      console.log('✅ getOffersCompleteReport funcionou:', offersReport);
    } catch (err) {
      console.log('❌ getOffersCompleteReport falhou:', err.message);
    }
    
    hideLoading();
    showNotification('Testes de conectividade concluídos! Verifique o console para detalhes.', 'success');
    
  } catch (error) {
    console.error('❌ [TESTE] Erro durante os testes:', error);
    hideLoading();
    showNotification(`Erro nos testes: ${error.message}`, 'error');
  }
}

// Função de debug rápido
function debugApiService() {
  console.log('🔍 [DEBUG] Informações sobre apiService:');
  console.log('- apiService existe?', typeof apiService !== 'undefined');
  console.log('- apiService é um objeto?', typeof apiService === 'object');
  if (typeof apiService === 'object' && apiService !== null) {
    console.log('- Métodos disponíveis:', Object.getOwnPropertyNames(Object.getPrototypeOf(apiService)));
  }
  console.log('- getCourseStatistics existe?', typeof apiService.getCourseStatistics === 'function');
  console.log('- getOffersCompleteReport existe?', typeof apiService.getOffersCompleteReport === 'function');
  
  return apiService;
}

// Teste rápido no console do browser
console.log('🚀 Arquivo de teste carregado! Use as funções:');
console.log('- debugApiService() - para debug básico');
console.log('- testBackendConnection() - para teste completo');