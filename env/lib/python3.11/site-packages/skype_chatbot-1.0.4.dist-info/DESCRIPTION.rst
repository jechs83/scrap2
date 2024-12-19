Python Skype Bot API for developing bots.   
More instructions you can find on GitHub: https://github.com/denissa4/skype_chatbot     
=====================================================================================     
For start using import skype_chatbot package:   
import skype_chatbot   
=====================================================================================    
Write you app ID and secret key:  
app_id = "example_app_id"   
app_secret = "example_app_secret"   
=====================================================================================    
Create object in source file:  
bot = skype_chatbot.SkypeBot(app_id, app_secret)
=====================================================================================    
Now you can use base methods:      
send_message                      
send_media                         
create_animation_card              
create_card_attachment             
create_card_image                 
create_buttons                    
send_card                           
create_card_adaptive               
create_item_for_adaptive_card      
create_action_for_adaptive_card   
=====================================================================================    
Send message:   
send_message(bot_id, bot_name, recipient, service, sender, text, text_format)

bot_id - skype bot id, you can get it from request data['recipient']['id'].     
  bot_name - skype bot name, you can get it from request data['recipient']['name'].     
  recipient - user, to whom you are sending the message. You can get it from request data['from'].     
  service - service url, you can get it from request data['serviceUrl'].     
  sender - conversation id, you can get it from request data['conversation']['id'].     
  text - text what you want to send recipient. Must be a string.     
  text_format - supported values: "plain", "markdown", or "xml" (default: "markdown").     
=====================================================================================    
Send media files:    
send_media(bot_id, bot_name, recipient, service, sender, message_type, url, attachment_name)

bot_id - skype bot id, you can get it from request data['recipient']['id'].     
bot_name - skype bot name, you can get it from request data['recipient']['name'].     
recipient - user, to whom you are sending the message. You can get it from request data['from'].     
service - service url, you can get it from request data['serviceUrl'].     
sender - conversation id, you can get it from request data['conversation']['id'].     
message_type - type of your media file, e.g. "image/png".     
url - open url for your media file.     
attachment_name - name, which is displayed to recipient.     
=====================================================================================    
Create card that can play animated GIFs or short videos:   
create_animation_card(card_type, url, images, title, subtitle, text, buttons, autoloop, autostart, shareable)

card_type - type of card attachment ("hero", "thumbnail", "receipt").     
  url - open url for your animation file.     
  images - list of images, in card attachment (to create image use method create_card_image). Must be a list.     
  title - title for your card. Must be a string.     
  subtitle - subtitle for your card. Must be a string.     
  text - text for your card. Must be a string.     
  buttons - list of buttons, in card attachment (to create button use method create_buttons). Must be a list.     
  autoloop - default: True.     
  autostart - default: True.     
  shareable - default: True.     
=====================================================================================    
Create card attachment("hero", "thumbnail", "receipt"):   
create_card_attachment(card_type, title, subtitle, text, images, buttons)

card_type - type of card attachment ("hero", "thumbnail", "receipt").     
  title - title for your card. Must be a string.     
  subtitle - subtitle for your card. Must be a string.     
  text - text for your card. Must be a string.     
  images - list of images, in card attachment (to create image use method create_card_image). Must be a list.     
  buttons - list of buttons, in card attachment (to create button use method create_buttons). Must be a list.     
=====================================================================================    
Create image for card:  
create_card_image(url, alt)

  url - open url for your image.     
  alt - alternative text for image.     
=====================================================================================    
Create button(actions) for card:   
create_button(button_type, title, value)

button_type - type of your button(e.g. "openUrl", "postBack").     
  title - name of button.     
  value - value of button(e.g. if button_type="openUrl", value="example.com").     
=====================================================================================    
Send card attachment to recipient:   
send_card(bot_id, bot_name, recipient, reply_to_id, service, sender, message_type, card_attachment, text)

bot_id - skype bot id, you can get it from request data['recipient']['id'].     
  bot_name - skype bot name, you can get it from request data['recipient']['name'].     
  reply_to_id - the message id you are replying to, you can get it from request data['id'].     
  recipient - user, to whom you are sending the message. You can get it from request data['from'].     
  service - service url, you can get it from request data['serviceUrl'].     
  sender - conversation id, you can get it from request data['conversation']['id'].     
  message_type - if you send more than one card, choose display way("carousel" or "list").     
  card_attachment - list of cards, in message (to create cards use method create_card_attachment). Must be a list.     
  text - text of your message.     
=====================================================================================    

