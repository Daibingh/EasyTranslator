# -*- mode: python -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['K:\\github\\EasyTranslator'],
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
a.datas += [('white.qss','K:\\github\\EasyTranslator\\white.qss','DATA'),
        ('dark.qss','K:\\github\\EasyTranslator\\dark.qss','DATA'),
			 ('google.png','K:\\github\\EasyTranslator\\google.png','DATA'),
			 ('baidu.png','K:\\github\\EasyTranslator\\baidu.png','DATA'),
			 ('bing.png','K:\\github\\EasyTranslator\\bing.png','DATA'),
			 ('powerword.png','K:\\github\\EasyTranslator\\powerword.png','DATA'),
			 ('youdao.png','K:\\github\\EasyTranslator\\youdao.png','DATA'),
			 ('cnki.png','K:\\github\\EasyTranslator\\cnki.png','DATA'),
			 ('icon.ico','K:\\github\\EasyTranslator\\icon.ico','DATA'),
       ('checkbox.png','K:\\github\\EasyTranslator\\checkbox.png','DATA')]
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
          console=False , icon='K:\\github\\EasyTranslator\\icon.ico')