from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
import os
import json

import ML_Updated_Copy


class S(BaseHTTPRequestHandler):

	# handle GET
    def do_GET(self):
        rootdir = os.getcwd() 
  
        try:
            print(rootdir + self.path)
            
            path = self.path.split("?",1)[0]
            if path == '/':
                self.path += 'index.html'   # default to index.html
                
            elif self.path.endswith('.html'):
                f = open(rootdir + self.path)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))  
                f.close()  
            elif self.path.endswith('.js'):
                f = open(rootdir + self.path)
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))  
                f.close()
            else:
                self.send_error(404, 'file not supported')  
                
        except IOError:
            self.send_error(404, 'file not found')  


	# handle POST
    def do_POST(self):
        rootdir = os.getcwd() 
  
        try:
            print(rootdir + self.path)
            
            path = self.path.split("?",1)[0]

            if path == '/apply':
			
                # JSON string
                application = self.rfile.read(int(self.headers['Content-Length']))
				
                ##########################################################################################
                # Python dictionary
                apply = json.loads(application)
                        
                ################################################################################################
                user_cat = str(apply['category'])
                user_maincat = str(apply['main_category'])
                user_days_elapsed = int(apply['days_elapsed'])
                user_usd_goal_real = int(apply['usd_goal_real'])
                user_country = str(apply['country'])
                user_month_launched = int(apply['month_launched'])


                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin","*")
                self.send_header("Access-Control-Allow-Methods","*")
                self.send_header("Access-Control-Allow-Headers","*")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                
                #########################################################################3############################
                ###################################################################################################3
                # call the prediction function in ml.py
                result = ML_Updated_Copy.predictState(user_cat,user_maincat,user_usd_goal_real,user_days_elapsed,user_country,user_month_launched)
                
                # make a dictionary from the result
                resultObj = { "result": result }
                
                # convert dictionary to JSON string
                resultString = json.dumps(resultObj)
                
                self.wfile.write(resultString.encode('utf-8'))
                
            else:
                self.send_error(404, 'endpoint not supported')  
                
        except IOError:
            self.send_error(404, 'endpoint not found')  
        

def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting server on {addr}:{port}")
    httpd.serve_forever()

   
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
    	"-l",
    	"--listen",
    	default="localhost",
    	help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
    	"-p",
    	"--port",
    	type=int,
    	default=8000,
    	help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    
        #################################################################################
    # train the model
 #   ml.train()
    
    # start the server
    run(addr=args.listen, port=args.port)