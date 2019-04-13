# -*- mode: python -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['/home/hdb/github/EasyTranslator'],
             binaries=[],
             datas= [],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas += [('white.qss','white.qss','DATA'),
			 ('google.png','google.png','DATA'),
			 ('baidu.png','baidu.png','DATA'),
			 ('bing.png','bing.png','DATA'),
			 ('powerword.png','powerword.png','DATA'),
			 ('youdao.png','youdao.png','DATA'),
			 ('cnki.png','cnki.png','DATA'),
			 ('icon.ico','icon.ico','DATA')]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='EasyTranslator',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='icon.ico')
