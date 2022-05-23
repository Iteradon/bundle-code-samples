import json
import struct

#  
# Used to connect and communicate with a bundle instance
#

class Client:

  def __init__(self, pipe_name):

    self.pipe = open('\\\\.\\pipe\\' + pipe_name, 'r+b', 0)
  
  #
  # Close the pipe to disconnect from the Bundle application.
  #
  
  def close(self):
    
    self.pipe.close()
    
  #
  # Send a json payload to the Bundle application.
  #
  
  def write(self, data):

     octets = json.dumps(data).encode("utf-8")
     
     # Send package length
     self.pipe.write(struct.pack('<i', len(octets)))
     
     # Send package
     self.pipe.write(octets)
    
  #
  # Read a response json payload from the Bundle application.
  #
  
  def read(self):

    INT_SIZE = 4
    
    # Read the length of the package
    buffer = self.pipe.read(INT_SIZE)
    if len(buffer) != INT_SIZE:
      raise IOError("%d bytes expected, but %d found" % (INT_SIZE, len(buffer)))
      
    size = struct.unpack('<i', buffer)[0]
    
    # Read and decode the package
    buffer = self.pipe.read(size)
    if len(buffer) != size:
      raise IOError("%d bytes expected, but %d found" % (size, len(buffer)))
      
    return json.loads(buffer.decode("utf-8"))
  
  #
  # Send a json payload to the Bundle application. Returns the first key in the
  # response that is not the status or message. Prints an error if the status
  # is not OK.
  #
  
  def send(self, data):
  
    self.write(data)
    response = self.read()

    if response['status'] == "OK":
      for key, value in response.items():
        if key != 'status' and key != 'message':
          return value      
    
    print(response['message'])
    exit(1)
    