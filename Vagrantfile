
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "bento/ubuntu-16.04-i386"

  config.vm.network :private_network, ip: "192.168.33.10"

  config.vm.synced_folder './', '/home/koukoku-system/'

  config.vm.provider 'virtualbox' do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = '2048'

  end

  config.vm.provision :shell, :path => "provisions/provision_root.sh", :privileged => true
  config.vm.provision :shell, :path => "provisions/provision_vagrant.sh", :privileged => false

end
