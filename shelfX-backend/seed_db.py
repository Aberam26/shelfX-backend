import os
import shutil
import MySQLdb

conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='book_haven')
cur = conn.cursor()

# 1. Clear old data (ignore foreign key checks temporarily)
cur.execute('SET FOREIGN_KEY_CHECKS = 0;')
cur.execute('TRUNCATE TABLE books;')
cur.execute('TRUNCATE TABLE authors;')
cur.execute('TRUNCATE TABLE categories;')
cur.execute('SET FOREIGN_KEY_CHECKS = 1;')

# 2. Insert Categories
categories = [
  ('3', 'Thriller | திகில் நாவல்கள்', 'thriller', 'Suspense and mystery'),
  ('4', 'Ancient | பண்டைய இலக்கியம்', 'ancient', 'Historical and classical literature'),
  ('5', 'Romance | காதல் நாவல்கள்', 'romance', 'Love stories and relationships'),
  ('7', 'Biography | வாழ்க்கை வரலாறுகள்', 'biography', 'Life stories of remarkable people'),
  ('8', 'Self-Help | சுய முன்னேற்ற நூல்கள்', 'self-help', 'Personal development and growth'),
  ('9', 'Poetry | கவிதைகள்', 'poetry-lyrics', 'Tamil poetry, lyrics and verse collections'),
  ('11', 'Travelogue | பயணக்குறிப்பு', 'travelogue', 'பயண அனுபவங்கள் மற்றும் கட்டுரைகள்')
]
for cat in categories:
    cur.execute('INSERT INTO categories (id, name, slug, description) VALUES (%s, %s, %s, %s)', cat)

# 3. Insert Authors
authors = [
  ('1', 'Na. Muthukumar', 'Renowned Tamil poet, lyricist, and author known for his soulful verses.', '/media/authors/na-muthukumar/na-muththukumar.jpg'),
  ('2', 'Lathah', 'Prominent writer exploring contemporary themes and human emotions.', '/media/authors/latha/Latha(3).jpg'),
  ('3', 'Manushyapuththiran', 'Modern Tamil poet and influential literature figure.', '/media/authors/manushya-puththiran/manushyaputran1.jpg'),
  ('4', 'Marudhan', 'Talented author known for deep narrative style and cultural insights.', '/media/authors/marudhan/marudhan.jpg'),
  ('5', 'P.S.V. Kumarasamy', 'Respected literary personality with a focus on historical and social themes.', '/media/authors/psv kumaraswamy/psv-kumaraswamy.jpg'),
  ('6', 'Yathiri', 'Creative storyteller bringing unique perspectives to Tamil literature.', '/media/authors/yathiri/yathiri.jpg'),
  ('7', 'S. Ramakrishnan', 'Highly acclaimed novelist, essayist, and screenwriter in modern Tamil literature.', '/media/authors/s.ramakrishnan/s.ramakrishnan.jpg'),
  ('8', 'Kalki', 'Legendary Tamil writer known for historical novels like Ponniyin Selvan.', '/media/authors/kalki/Kalki.jpg'),
  ('9', 'Sujatha', 'Prolific Tamil writer known for science fiction and modern thrillers.', '/media/authors/sujatha/sujatha.jpg'),
  ('10', 'Jeyakanthan', 'Powerful voice in Tamil literature, known for his realistic portrayal of society.', '/media/authors/jeyakanthan/jeyakanthan.jpg'),
  ('11', 'Gobinath', 'Popular television host and author known for his motivational works.', '/media/authors/gobinath/gobinath.jpg')
]
for author in authors:
    cur.execute('INSERT INTO authors (id, name, bio, image) VALUES (%s, %s, %s, %s)', author)

# 4. Insert Books
books = [
  ('1', 'Kanpesum Varthaigal', '1', '9', 150.0, None, '/media/books/na-muthukumar/kanpesum-varthaigal-na-muththukumar.jpeg', 'A soul-stirring collection of lyrics and verses by the legendary Tamil poet and lyricist Na. Muthukumar, capturing the depths of human emotion through the beauty of Tamil words.', 50, 4.8, 320, 1200, 4500, '2024-01-01', '978-81-000-0001-1', 180, 'Kizhakku Pathippagam', 'Tamil'),
  ('2', 'கழிவறை இருக்கை', '2', '8', 214.0, 225.0, '/media/books/lathah/kalivarai-irukkai-lathah.jpeg', 'பாலியல், பெண்கள் மற்றும் பெண்ணியம் குறித்த தைரியமான கட்டுரைகளின் தொகுப்பு. லதாவின் வலிமையான எழுத்து சமூகத்தின் மறைக்கப்பட்ட உண்மைகளை அம்பலப்படுத்துகிறது.', 30, 4.5, 2, 500, 2000, '2020-12-01', '978-81-000-0002-2', 224, 'Knowrap Imprints', 'Tamil'),
  ('3', 'என்னை நினைத்துக் கொண்டதற்கு நன்றி', '3', '9', 120.0, None, '/media/books/manushyapuththiran/yennai-ninaiththu-kondatharku-nanri-10023096-1000x1000h.jpeg', 'என்னோடிருக்கலாமே என்ரு துவங்கிய கோரிக்கைகள் என்னையும் கொஞ்சம் நினைத்துகொள்ளலாமே என்று இறைஞ்சுதலாக எஞ்சுவதற்குத்தான் இத்தனை மயக்கங்களா?', 40, 4.7, 85, 900, 3200, '2023-01-01', '978-81-000-0003-3', 120, 'உயிர்மை வெளியீடு', 'Tamil'),
  ('4', 'மர்ம முத்தம்', '3', '9', 120.0, None, '/media/books/manushyapuththiran/marma-mutham-10024952-1000x1000h.jpeg', 'மனுஷ்ய புத்திரனின் கவிதைகள் உள்ளத்தின் மறைபொருளான உணர்வுகளை மர்ம முத்தமென தொட்டுச் செல்கின்றன.', 35, 4.6, 60, 750, 2800, '2023-01-01', '978-81-000-0004-4', 128, 'உயிர்மை பதிப்பகம்', 'Tamil'),
  ('7', 'சே குவேரா: வேண்ொும் விடுதலை!', '4', '7', 180.0, 190.0, '/media/books/marudhan/che-guevara-vendum-viduthalai_FrontImage_563.jpg', 'வாழ்க்கை முழுவதும் யுத்தங்கள்! போராட்டங்கள்! லத்தீன் அமெரிக்க நாடுகள் அனைத்தையும் அடிமைத் தளையிலிருந்து விடுவிக்கும் வேட்கை. சே ஒரு தனிமனிதரல்லர் ஆ மாபெரும் நிலப்பரப்பின் மனச்சாட்சி. விடுதலை வேட்கை உள்ள அனைவருக்கும் உந்துசக்தியாக விளங்கும் சே குவேராவின் விறுவிறுப்பான வாழ்க்கைவரலாறு இந்நூல்.', 40, 4.6, 28, 950, 3800, '2006-01-01', '9788183682442', 160, 'கிழக்கு பதிப்பகம்', 'Tamil'),
  ('8', 'Mossad (மொசாட்)', '5', '3', 520.0, None, '/media/books/psv-kumarasamy/mosaad_tamil.jpg', 'இச்ரேலின் இரகசியப் பாதுகாப்பு அமைப்பான \'மொசாட்\'தான் உலகிலேயே தலைசிறந்த புலனாய்வு அமைப்பு. அறுபதாண்டுகால வரலாறு. நாஜி கொலைகாரனின் கடத்தலில் தொடங்கி ஈரானிய அணுசக்தி அறிவியலறிஞர்களின் களையெடுப்புவரை, ஹாலிவுட் திரைப்படங்களை விஞ்சி நிற்கும் உண்மையான சாகஜக் கதைகள்.', 35, 4.8, 7, 1100, 4200, '2023-06-21', '978-81-000-0008-8', 520, 'Manjul Publishing House Pvt Ltd', 'Tamil'),
  ('6', 'காதலே கதிமோட்சம்', '6', '9', 114.0, 120.0, '/media/books/yathiri/kaadhale-gathimotcham_FrontImage_886.jpg', 'காதலிக்க மறுத்த பெண்ணை, காதலிலிருந்து விலகிய பெண்ணை ஆசிர்வதிக்குமெனும் நப்பாசையுடன் எழுதப்பட்ட கவிதைகள். அன்பின் உச்சம் வன்முறையாக மாறும் வலி முறைகளையும் சமநிலைப்படுத்த வேண்டும் என்ற எதிர்பார்ப்புடன் யாத்திரி எழுதுகிறார்.', 40, 4.4, 12, 600, 2500, '2019-01-01', '978-81-000-0006-6', 112, 'வாசகசாலை', 'Tamil'),
  ('9', 'தேசாந்திரி', '7', '11', 261.0, 275.0, '/media/books/s-ramakrishnan/desanthiri-10014329-1000x1000h.jpeg', 'சுதந்திரத்தோடு தேடல் மனம்கொண்ட மனிதர்கள் உலகத்தை அறியத் துடிக்கிறார்கள். மலைகள், ஆறுகள், அருவிகள், பாலைவனம், வரலாற்றுச் சின்னங்கள் ஆகியவற்றை எழுத்தோவியங்களால் ரசிக்க வைக்கிறார் எஸ்.ராமகிருஷ்ணன். ஆனந்த விகடனில் \'தேசாந்திரி\'யாக வாசகர்களுடன் பகிர்ந்த அற்புத அனுபவங்கள்.', 45, 4.7, 0, 1300, 5000, '2019-01-01', '9789387484566', 256, 'தேசாந்திரி பதிப்பகம்', 'Tamil'),
  ('11', 'பொன்னியின் செல்வன்', '8', '4', 1140.0, 1200.0, '/media/books/kalki/ponniyin-selvan-10022133-1100x1100h.jpeg', 'தமிழ் இலக்கியத்தின் மொழியிலான மாபெரும் சரித்திர நாவல். சோழ மரபின் பொற்காலத்தில் நடக்கும் இராஜத்துவங்கள், போர்கள், காதல், வீரம், தியாகம் ஆகியவ்றை இற்கையொடு சித்திரிக்கிறார் கல்கி. தமிழ் கிளாச்சிக் முதன்மைப் படைப்புகளில் ஒன்றான் ஈ வடிவ வற்று பதிப்பு.', 25, 4.9, 0, 3500, 12000, '2022-10-01', '9788194346524', 1424, 'டிஸ்கவரி புக் பேலஸ்', 'Tamil'),
  ('5', 'மேலும் ஒரு குற்றம்', '9', '3', 152.0, 160.0, '/media/books/sujatha/melum-oru-kuttam-1000x1000h.jpg', 'கணேஷ்-வசந்த் இடம் பெறும் \'மேலும் ஒரு குற்றம்\'. மெர்க்காராவின் காஃபி எஸ்டேட் முதலாளி ஒருவரிடமிருந்து கணேஷுக்கு அழைப்பு வருகிறது — \'சும்மா ஜாலியா என்னோட செஸ் ஆட வாங்க!\' புதிரான சதுரங்கம் மற்றும் மறைமுகமான சவாலும் கல்ந்த நிறைந்த தொடர்.', 45, 4.5, 0, 800, 3000, '2010-01-01', '9788184935905', 112, 'கிழக்கு பதிப்பகம்', 'Tamil'),
  ('10', 'சில நேரங்களில் சில மனிதர்கள்', '10', '5', 200.0, None, '/media/books/jeyakanthan/jeyakaanthan.jpg', 'வெகுஜன தளத்தில் இலக்கியபூர்வமான அதிர்வுகளை ஏற்படுத்திய எழுத்தாளர் ஜெயகாந்தனின் முதன்மையான நாவல். தன்னுடையதல்லாத காரணத்தால் பழிக்கு ஆளான பெண்ணைப் போதுச்சமூகம் எவ்வளவு துச்சமாக மதிக்கிறது என்பதையும், அவள் தனது சுயமரியாதையால் எதிர்கொள்ளும் விதத்தையும் பரிவுடன் சித்திரிக்கிறார் ஜெயகாந்தன். காலங்கடந்தும் நிலைபெறும் ஒரு கிளாச்சிக் முதன்மைப் படைப்பு.', 50, 4.8, 145, 5000, 18000, '2014-12-01', '978-9384641016', 200, 'Kalachuvadu Publications', 'Tamil'),
  ('12', 'ப்ளீஸ்! இந்த புத்தகத்தை வாங்காதீங்க', '11', '8', 168.0, 177.0, '/media/books/gobinath/please-intha-puththagaththai-vaangaatheenga_FrontImage_662.jpg', 'ப்ளீஸ்! இந்த புத்தகத்தை வாங்காதீங்க ஏன்னா இந்த புத்தகத்தில் நான் எதையும் புதிதாக சொல்லிவிடவில்லை என்று முன்னுரையில் ஆரம்பித்த ஆசிரியர், ஒரே மூச்சில் முழுவதும் படிக்கும்படி செய்துள்ளார். உங்களுக்கு உங்களை அடையாளம் காட்டும், உங்கள் சிறப்பியல்புகளையும் திறனின் நீள அகலங்களையும் எளிமையான உதாரணங்கள் மூலம் புரியவைத்துள்ளார் கோபி!', 60, 4.6, 38, 2200, 8500, '2013-01-01', '9788192465722', 112, 'சிக்ஸ்த் சென்ஸ் பப்ளிகேஷன்ஸ்', 'Tamil')
]
for book in books:
    cur.execute('INSERT INTO books (id, title, author_id, category_id, price, original_price, cover, description, stock, rating, review_count, sales_count, view_count, created_at, isbn, pages, publisher, language) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', book)

conn.commit()
print('Successfully seeded database with Tamil books!')

# 5. Copy media files
src_dir = r'd:\shelfx\shelfX-frontend\src\assets\images'
dst_dir = r'd:\shelfx\shelfX-django\media'
if os.path.exists(src_dir):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)
    print(f'Copied media from {src_dir} to {dst_dir}')
else:
    print(f'Source dir {src_dir} not found!')
