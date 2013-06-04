KTHNXBAI Gallery
----------------

See requirements.txt for required modules

This is the source for http://www.kthnxbai.co.uk

A very simple image gallery primarily used to collect images off of
the rest of the internet and to share them.

What to do
----------

First configure the settings in 

    configs/exampleconfig.py
  
The ORM is SQLAlchemy, so you can use PostgreSQL, MySQL or SQLite.

The way to import images is to create a 'to_process' folder in the 
project root and then put all the images you want to import into that 
folder. Then run 

    python manage.py ingest_images
  
and it will create thumbnails, determine if the image is animated and
import the data into the database. Thumbnails and original images are 
then moved to the path set by the IMAGE_PATH config variable.

Other
-----

First flask project, so still ironing out some layout and design

License
-------

Licensed under the BSD 3-Clause License.

Copyright (c) 2013, Sven Steinbauer
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list 
of conditions and the following disclaimer. Redistributions in binary form must 
reproduce the above copyright notice, this list of conditions and the following 
disclaimer in the documentation and/or other materials provided with the distribution.

Neither the name of the author nor the names of its contributors may be used to endorse 
or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR 
TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
