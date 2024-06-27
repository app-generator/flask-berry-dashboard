# open chatbot in background then run flask
cd "/Users/barry.walsh/rotaready/rr_repos/salesfc-api-e2e/apps/genai-vite/ldfe-genai-demo" 
npm run dev & 
cd "/Users/barry.walsh/rotaready/rr_repos/salesfc-api-e2e" 
flask run -h localhost -p 5002
