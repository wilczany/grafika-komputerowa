require "gtk3"

# window = Gtk::Window.new("First example")
# window.set_size_request(400, 400)
# window.set_border_width(10)
# window.

# button = Gtk::Button.new(:label => "Say hello")
# button.signal_connect "clicked" do |_widget|
#   puts "Hello World!!"
# end

# window.add(button)
# window.signal_connect("delete-event") { |_widget| Gtk.main_quit }
# window.show_all

# Gtk.main
# 
 
app = Gtk::Application.new("org.gtk.example", :flags_none)

app.signal_connect "activate" do |application|
  window = Gtk::ApplicationWindow.new(application)
  window.set_title("Window")
  window.set_default_size(200, 200)

  button_box = Gtk::ButtonBox.new(:horizontal)
  window.add(button_box)

  button = Gtk::Button.new(label: "Hello World")
  button.signal_connect "clicked" do |widget|
    puts "Hello World"
    window.destroy
  end

  button_box.add(button)

  window.show_all
end

puts app.run