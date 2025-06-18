describe('Login Flow', () => {
  it('should login and show dashboard with welcome text', () => {
    // Login via API and set cookie
    cy.request('POST', 'http://localhost:8000/auth/jwt/login', {
      username: 'demo@example.com',
      password: 'demo'
    }).then((response) => {
      // Extract cookie from response headers
      const setCookieHeader = response.headers['set-cookie'];
      if (setCookieHeader) {
        // Handle both string and array types
        const cookieHeader = Array.isArray(setCookieHeader) ? setCookieHeader[0] : setCookieHeader;
        const cookieMatch = cookieHeader.match(/crm-auth=([^;]+)/);
        if (cookieMatch) {
          const cookieValue = cookieMatch[1];
          cy.setCookie('crm-auth', cookieValue);
        }
      }
      
      // Visit dashboard
      cy.visit('/dashboard');
      
      // Verify welcome text appears
      cy.contains('Welcome');
      
      // Verify cookie is set
      cy.getCookie('crm-auth').should('exist');
    });
  });

  it('should redirect to login when accessing dashboard without auth', () => {
    // Clear any existing cookies
    cy.clearCookies();
    
    // Try to visit dashboard
    cy.visit('/dashboard');
    
    // Should be redirected to login page
    cy.url().should('include', '/login');
  });

  it('should show user email in dashboard after login', () => {
    // Login via API and set cookie
    cy.request('POST', 'http://localhost:8000/auth/jwt/login', {
      username: 'demo@example.com',
      password: 'demo'
    }).then((response) => {
      const setCookieHeader = response.headers['set-cookie'];
      if (setCookieHeader) {
        // Handle both string and array types
        const cookieHeader = Array.isArray(setCookieHeader) ? setCookieHeader[0] : setCookieHeader;
        const cookieMatch = cookieHeader.match(/crm-auth=([^;]+)/);
        if (cookieMatch) {
          const cookieValue = cookieMatch[1];
          cy.setCookie('crm-auth', cookieValue);
        }
      }
      
      // Visit dashboard
      cy.visit('/dashboard');
      
      // Verify user email is displayed
      cy.contains('demo@example.com');
      
      // Verify avatar menu is present
      cy.get('[data-testid="avatar-menu"]').should('exist');
    });
  });
}); 