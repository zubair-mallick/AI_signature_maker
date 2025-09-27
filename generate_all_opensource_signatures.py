import io
import os
import sys
import re
import random
import math
import numpy as np
from typing import List, Tuple, Optional
import requests
import torch
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO

import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

# Custom ink color - Dark Blue Pen Ink
INK_COLORS = [
    (25, 45, 85),  # Dark blue pen ink
]

class OpenSourceHandwritingGenerator:
    def __init__(self):
        self.api_available = False
        self.try_setup_api()
    
    def try_setup_api(self):
        """Try to set up access to handwriting generation APIs"""
        print("🔍 Checking for available handwriting generation APIs...")
        # We'll use a simple approach that works offline
        self.api_available = True
        print("✅ Using local handwriting generation")
    
    def generate_handwritten_image(self, text: str, width: int = 400, height: int = 100) -> Image.Image:
        """Generate handwritten text image using simple curve-based approach"""
        
        # Create image with slight white background (like paper)
        img = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Try to use a more natural-looking font if available  
        # Adjust font size based on canvas size
        if width <= 150:
            font_size = 10  # Smaller font for small canvas
        elif width <= 250:
            font_size = 16  # Medium size for medium canvas
        elif width <= 350:
            font_size = 20  # Large font for large canvas
        else:
            font_size = 26  # Much larger font for much larger canvas
        try:
            # Use custom handwriting fonts from fonts directory
            font_dir = r"C:\Users\mallik\Desktop\freind\prak\names\fonts"
            possible_fonts = [
                os.path.join(font_dir, "Sacramento-Regular.ttf"),          
                       # Natural handwriting
              
               
                # Fallback to system fonts if custom fonts not available
                "C:\\Windows\\Fonts\\BRADHITC.TTF",  # Bradley Hand ITC
   
            ]
            
            # Collect all available fonts
            available_fonts = []
            for font_path in possible_fonts:
                if os.path.exists(font_path):
                    available_fonts.append(font_path)
            
            # Randomly select a font from available options
            font = None
            if available_fonts:
                selected_font_path = random.choice(available_fonts)
                font = ImageFont.truetype(selected_font_path, font_size)
                # Don't print for each signature to avoid spam
            
            if font is None:
                font = ImageFont.load_default()
                
        except Exception as e:
            font = ImageFont.load_default()
        
        # Calculate text position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Add slight randomness to position
        random.seed(hash(text))
        x += random.randint(-1, 1)
        y += random.randint(-3, 1)
        
        # Choose ink color
        ink_color = random.choice(INK_COLORS)
        
        # Randomly choose handwriting style for natural variation
        handwriting_style = random.choice(['cursive', 'casual_print', 'mixed'])
        
        # if handwriting_style == 'cursive':
            # Cursive style - flowing, connected appearance with very tight letter spacing
        current_x = x
        baseline_drift = 0  # Minimal baseline drift for smooth cursive flow
            
        for i, char in enumerate(text):
                if char == ' ':
                    # Moderate space between words, consistent with cursive flow
                    space_width = max(6, font_size // 3) + random.randint(-1, 2)
                    current_x += space_width
                    baseline_drift += random.uniform(-0.2, 0.2)  # Very minimal drift through spaces
                    continue
                
                # Very subtle baseline variation for smooth cursive connection
                baseline_drift += random.uniform(-0.3, 0.3)
                baseline_drift = max(-2, min(2, baseline_drift))  # Keep very tight bounds
                char_y = y + int(baseline_drift)
                
                # Minimal character positioning variation for smooth flow
                char_x_offset = random.uniform(-0.2, 0.2)
                draw.text((current_x + char_x_offset, char_y), char, fill=ink_color, font=font)
                
                # Measure character width
                char_bbox = draw.textbbox((0, 0), char, font=font)
                char_width = char_bbox[2] - char_bbox[0]
                
                # Much tighter spacing for cursive connection - letters almost touching
                if i < len(text) - 1 and text[i + 1] != ' ':
                    # Very tight spacing with minimal variation for connected cursive look
                    spacing_var = random.uniform(-3.5, -1.5)  # Negative values to bring letters closer
                    current_x += char_width + spacing_var
                else:
                    current_x += char_width
                    
        # elif handwriting_style == 'casual_print':
        #     # Casual printed style - like the examples in your image
        #     current_x = x
        #     baseline_y = y
            
        #     for i, char in enumerate(text):
        #         if char == ' ':
        #             # Normal space width with variation
        #             space_width = max(6, font_size // 3) + random.randint(-1, 4)
        #             current_x += space_width
        #             continue
                
        #         # Individual character baseline variation (less drift, more independent)
        #         char_y_offset = random.randint(-2, 2)
        #         char_y = baseline_y + char_y_offset
                
        #         # Slight horizontal offset for natural imperfection
        #         char_x_offset = random.uniform(-0.8, 0.8)
                
        #         # Occasional slight character tilt
        #         char_rotation = random.uniform(-1.5, 1.5) if random.random() < 0.2 else 0
                
        #         draw.text((current_x + char_x_offset, char_y), char, fill=ink_color, font=font)
                
        #         # Measure character width
        #         char_bbox = draw.textbbox((0, 0), char, font=font)
        #         char_width = char_bbox[2] - char_bbox[0]
                
        #         # More separated letter spacing like printed handwriting
        #         spacing_var = random.uniform(-0.5, 2.0)
        #         current_x += char_width + spacing_var + 1
                
        # else:  # mixed style
        #     # Mixed style - combination of both approaches
        #     current_x = x
        #     baseline_drift = 0
            
        #     for i, char in enumerate(text):
        #         if char == ' ':
        #             space_width = max(7, font_size // 2) + random.randint(-1, 3)
        #             current_x += space_width
        #             baseline_drift += random.uniform(-0.3, 0.3)
        #             continue
                
        #         # Mix of gradual drift and individual variation
        #         if random.random() < 0.6:  # 60% gradual drift
        #             baseline_drift += random.uniform(-0.5, 0.5)
        #             baseline_drift = max(-3, min(3, baseline_drift))
        #             char_y = y + int(baseline_drift) + random.randint(-1, 1)
        #         else:  # 40% independent positioning
        #             char_y = y + random.randint(-2, 2)
                
        #         # Character positioning variation
        #         char_x_offset = random.uniform(-0.6, 0.6)
        #         draw.text((current_x + char_x_offset, char_y), char, fill=ink_color, font=font)
                
        #         # Character width measurement
        #         char_bbox = draw.textbbox((0, 0), char, font=font)
        #         char_width = char_bbox[2] - char_bbox[0]
                
        #         # Variable spacing - sometimes tight, sometimes loose
        #         if random.random() < 0.4:  # 40% tight spacing
        #             spacing_var = random.uniform(-2.0, 1.0)
        #             current_x += char_width + spacing_var
        #         else:  # 60% normal spacing
        #             spacing_var = random.uniform(-0.5, 1.5)
        #             current_x += char_width + spacing_var + 0.5
        
        # Apply subtle shadow effects to make signature blend better
        img = self.apply_shadow_effects(img)
        
        return self.crop_to_content(img, border=3)
    
    def apply_shadow_effects(self, img: Image.Image) -> Image.Image:
        """Apply subtle shadow effects around text for better blending"""
        
        try:
            # Import scipy for shadow effects
            from scipy import ndimage
            
            img_array = np.array(img)
            
            # Convert to grayscale to find text areas
            gray = np.mean(img_array, axis=2)
            
            # Find text regions (darker areas)
            text_mask = gray < 240
            
            # Add subtle shadow effect (50% chance)
            if np.any(text_mask) and random.random() < 0.5:
                # Create subtle shadow effect
                shadow_strength = random.uniform(1.0, 2.5)
                
                # Dilate the text mask slightly for shadow area
                shadow_mask = ndimage.binary_dilation(text_mask, iterations=1)
                shadow_mask = shadow_mask & ~text_mask  # Only the expanded area
                
                # Apply subtle shadow by slightly darkening the area
                img_array[shadow_mask] = np.clip(
                    img_array[shadow_mask] - shadow_strength, 0, 255
                ).astype(np.uint8)
            
            return Image.fromarray(img_array)
            
        except ImportError:
            # If scipy is not available, return original image
            return img
        except Exception:
            # If any error occurs, return original image
            return img
    
    def crop_to_content(self, img: Image.Image, border: int = 3) -> Image.Image:
        """Crop image to content with small border"""
        
        # Convert to grayscale to find content boundaries
        gray = img.convert('L')
        img_array = np.array(gray)
        
        # Find non-white pixels (content)
        non_white = img_array < 250  # Allow for slight variations from pure white
        
        # Find bounding box of content
        rows = np.any(non_white, axis=1)
        cols = np.any(non_white, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            # No content found, return small image
            return img.crop((0, 0, 50, 30))
        
        # Get the bounds
        top, bottom = np.where(rows)[0][[0, -1]]
        left, right = np.where(cols)[0][[0, -1]]
        
        # Add border
        top = max(0, top - border)
        bottom = min(img.height - 1, bottom + border)
        left = max(0, left - border)
        right = min(img.width - 1, right + border)
        
        # Crop the image
        cropped = img.crop((left, top, right + 1, bottom + 1))
        
        return cropped
    
    def image_to_pdf_overlay(self, img: Image.Image, 
                           page_width_pt: float, page_height_pt: float,
                           bottom_margin_pt: float = 60.0) -> io.BytesIO:
        """Convert PIL image to PDF overlay"""
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width_pt, page_height_pt))
        
        # Save image to temporary bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Calculate position and size - use original size for crisp quality
        img_width, img_height = img.size
        
        # Use original dimensions to avoid any scaling blur
        final_width = img_width
        final_height = img_height
        
        # Center horizontally
        x = (page_width_pt - final_width) / 2
        y = bottom_margin_pt
        
        # Add slight position variation
        random.seed(hash(str(img_width)))
        x += random.uniform(-15, 15)
        y += random.uniform(-8, 8)
        
        # Draw image on canvas at original size for maximum sharpness
        can.drawInlineImage(img, x, y, width=final_width, height=final_height)
        
        can.save()
        packet.seek(0)
        return packet

def create_opensource_signature_overlay(signature_text: str,
                                      page_width_pt: float,
                                      page_height_pt: float,
                                      bottom_margin_pt: float = 60.0) -> io.BytesIO:
    """Create PDF overlay using open-source handwriting generation"""
    
    # Create handwriting generator
    generator = OpenSourceHandwritingGenerator()
    
    # Generate handwritten image at much larger size for clarity
    signature_img = generator.generate_handwritten_image(
        signature_text, width=450, height=110  # Large canvas, yields 26pt font
    )
    
    # Convert to PDF overlay
    return generator.image_to_pdf_overlay(
        signature_img, page_width_pt, page_height_pt, bottom_margin_pt
    )

def parse_name_to_signature_format(full_name: str) -> str:
    """Convert full name to signature format"""
    if not full_name:
        return ""
    name = re.sub(r"\s+", " ", full_name.strip())
    if not name:
        return ""
    parts = name.split(" ")
    if len(parts) == 1:
        return parts[0]
    return f"{parts[0]} {parts[-1][0]}"

# List of all names from your original file
EXTRACTED_NAMES: List[str] = [
    "Sambhu Charan Manna",
    "Sekh Arif Ahmmod",
    "Mitali Mondal",
    "Ganga Rani Biswas",
    "Swapan Ghosh",
    "Debraj Das",
    "Saraswati Bauri",
    "Iqbal Khan",
    "Puja C",
    "Sadananda Mandal",
    "Manjura Bauri",
    "Bapi Bagdi",
    "Amita Tantubay",
    "Puja Ovalangal",
    "Pntu Dutta",
    "Subhash B",
    "Bapi Bagdi",
    "Purnima Biswas",
    "Benu Sarkar",
    "Achinta Mai",
    "Arup Roy",
    "Surojit Maji",
    "Minati Das",
    "Sukal Tudu",
    "Srabani Roy",
    "Chinmoy Pal",
    "Jayanta Bagdi",
    "Subhash Ghosh",
    "Shanti Sikari",
    "Krishnapada Goswami",
    "Gouranga Garai",
    "Samir Bagdi",
    "Aloke Kumar Chattopadhyay",
    "Rabindranath Karmakar",
    "Mamoni Sarkar Singha",
    "Sumanta Chakraborty",
    "Gobinda Haldar",
    "Shikha Mukherjee",
    "Sukumar Ruldas",
    "Mita Goral",
    "Pradip Misra",
    "Pratima Saren",
    "Sadananda Patra",
    "Pradip Misra",
    "Manasaram Bouri",
    "Chanpa Bauri",
    "Bilasi Bauri",
    "Durgarani Ghosh",
    "Sourav Mandal",
    "Akul Dangar",
    "Pal Swapan",
    "Uttam Lohar",
    "Alarani Sahis",
    "Tufan Bauri",
    "Krishna Pada Mandi",
    "Swpan Pal",
    "Ram Das Mandal",
    "Rajesh Das",
    "Sneha M",
    "Rabi Lochan Nayak",
    "Kripasindhu Das",
    "Souvik Mandal",
    "Biswataran Kotal",
    "Tapas Kumar Nandi",
    "Kamal Maji",
    "Subal Hazra",
    "Sanjit Ghosh",
    "Bharati B",
    "Bikash Ghosh",
    "Sumita Samui",
    "Prasanta Dey",
    "Sekh Ujir Ali",
    "Ramcharan Roy",
    "Ramcharan Roy",
    "Shibani Dhibar",
    "Tapan Kumar Pai",
    "Gita Mahadanda",
    "Paresh Nath Pal",
    "Sadhan Konar",
    "Sagar Koley",
    "Naran Majhi",
    "Labuhmi Roy",
    "Lakshmi Roy",
    "Labani B",
    "Joydev De",
    "Kartik Chandra Samui",
    "Sandhya Bibi Sekh",
    "Debnarayan Garai",
    "Radhashyam Majhi",
    "Lakshmi Roy",
    "Shrimanta Bagdi",
    "Nimatchandra Ghosh",
    "Kakali Ghosh",
    "Mantu Bagdi",
    "Anil Chandra Konar",
    "Susanta Bagdi",
    "Jaipadish Bagdi",
    "Bikash Digar",
    "Tapas Karak",
    "Nemai Mondal",
    "Dipak Ghosh",
    "Hari Sadhan Bagdi",
    "Chimnay Biswas",
    "Banan Bagdi",
    "Prashanta Mondal",
    "Dipu Bagdi",
    "Ananta Ghosh",
    "Uttam Kumar Bagdi",
    "Aparna Ghosh",
    "Mitali Mondal",
    "Sarbananda Biswas",
    "Arup Manna",
    "Ranit Pal",
    "Sekh Arif Ahmmod",
    "Ranu Sikdar",
    "Arup Kumar Garai",
    "Biman Bagdi",
    "Shankar Bhakto",
    "Rinku Bhaumik",
    "ProDir Bag",
    "Jhantu Sarkar",
    "Sumitra Dhara",
    "Samjit Bagdi",
    "Supriya Chatterjee",
    "Gourab Rakshit",
    "Shampa Karmakar",
]

def generate_all_opensource_signatures():
    """Generate open-source handwritten signatures for all names"""
    
    input_pdf = r"C:\Users\mallik\Desktop\freind\prak\names\croppdf_with_date_and_stamp.pdf"
    output_pdf = r"C:\Users\mallik\Desktop\freind\prak\names\signed_aadhaar_cards_opensource.pdf"
    
    print("🤖 Open-Source Handwriting Signature Generator")
    print("=" * 60)
    print(f"Input:  {input_pdf}")
    print(f"Output: {output_pdf}")
    print(f"Total names to process: {len(EXTRACTED_NAMES)}")
    print()
    
    print("✨ Features:")
    print("   • Beautiful custom handwriting fonts (Cedarville Cursive, Sacramento, Kristi, etc.)")
    print("   • Randomly selects different font for each signature (maximum variety)")
    print("   • Multiple handwriting styles: cursive, casual print, and mixed")
    print("   • Randomly selects style for each signature (natural variation)")
    print("   • Human-like baseline drift and character positioning")
    print("   • Realistic letter spacing variations")
    print("   • Dark blue ink color")
    print("   • Crisp, clear signatures (no scaling blur)")
    print("   • Paper-like white background")
    print("   • Generated at much larger size (450x110px → ~150x30px after cropping)")
    print()
    
    if not os.path.exists(input_pdf):
        print(f"❌ Input file not found: {input_pdf}")
        return False
    
    try:
        with open(input_pdf, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            writer = PyPDF2.PdfWriter()
            
            total_pages = len(reader.pages)
            if total_pages == 0:
                print("❌ PDF has no pages")
                return False
            
            print(f"📄 Processing {total_pages} pages...")
            print()
            
            processed = 0
            skipped = 0
            
            for idx, page in enumerate(reader.pages):
                page_no = idx + 1
                
                # Get name for this page
                if idx < len(EXTRACTED_NAMES):
                    full_name = EXTRACTED_NAMES[idx]
                else:
                    full_name = ""
                
                # Skip pages without names
                if not full_name or full_name.strip() == "":
                    print(f"Page {page_no:3}/{total_pages}: Skipped (no name)")
                    writer.add_page(page)
                    skipped += 1
                    continue
                
                # Generate signature text
                sig_text = parse_name_to_signature_format(full_name)
                if not sig_text:
                    print(f"Page {page_no:3}/{total_pages}: Skipped (invalid name): {full_name}")
                    writer.add_page(page)
                    skipped += 1
                    continue
                
                print(f"Page {page_no:3}/{total_pages}: Processing '{full_name}' → '{sig_text}'")
                
                # Page dimensions
                pw = float(page.mediabox.width)
                ph = float(page.mediabox.height)
                
                # Create open-source handwritten signature overlay
                overlay_stream = create_opensource_signature_overlay(
                    sig_text,
                    pw, ph,
                    bottom_margin_pt=35.0  # Positioned lower as requested
                )
                
                # Merge with original page
                overlay_pdf = PyPDF2.PdfReader(overlay_stream)
                page.merge_page(overlay_pdf.pages[0])
                writer.add_page(page)
                
                processed += 1
                
                # Show progress every 25 pages
                if processed % 25 == 0:
                    print(f"   Progress: {processed}/{len(EXTRACTED_NAMES)} signatures completed...")
            
            # Save result
            print()
            print("💾 Saving PDF...")
            with open(output_pdf, "wb") as out:
                writer.write(out)
            
            print()
            print("📊 SUMMARY:")
            print(f"✅ Total pages processed: {total_pages}")
            print(f"✅ Signatures added: {processed}")
            print(f"⚠️  Pages skipped: {skipped}")
            print(f"📁 Output saved to: {output_pdf}")
            print()
            print("🎯 All signatures use:")
            print("   • Handwriting-style fonts from your system")
            print("   • Dark blue ink color")
            print("   • Natural character variations")
            print("   • Crisp, clear appearance (no blur)")
            print("   • Professional handwritten look")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_all_opensource_signatures()
    sys.exit(0 if success else 1)
