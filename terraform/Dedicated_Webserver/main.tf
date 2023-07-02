terraform {
  required_version = ">= 1.1.0"
  required_providers {
    proxmox = {
      source = "telmate/proxmox"
      # version = "2.9.11"
      version = "2.9.10"
    }
  }
}

provider "proxmox" {
  # url is the hostname (FQDN if you have one) for the proxmox host you'd like to connect to to issue the commands. my proxmox host is 'prox-1u'. Add /api2/json at the end for the API
  pm_api_url = "https://datacenter.ramfield.net/api2/json"
  # api token id is in the form of: <username>@pam!<tokenId>
  pm_api_token_id = "terraform@mother_land!terraform"
  # this is the full secret wrapped in quotes. don't worry, I've already deleted this from my proxmox cluster by the time you read this post
  pm_api_token_secret = "5af5ebf3-1050-4439-a1f4-16a09eb500f0"
  # leave tls_insecure set to true unless you have your proxmox SSL certificate situation fully sorted out (if you do, you will know)
  pm_tls_insecure = false
  
  pm_log_enable = true
  pm_log_file   = "terraform-plugin-proxmox.log"
  pm_debug      = true
  pm_log_levels = {
    _default    = "debug"
    _capturelog = ""
  }
}
# resource is formatted to be "[type]" "[entity_name]" so in this case
# we are looking to create a proxmox_vm_qemu entity named test_server
resource "proxmox_vm_qemu" "Dedicated-Machine" {
  count = 2
  name = "Artisan-Dedicated-${count.index +1}" #count.index starts at 0, so + 1 means this VM will be named test-vm-1 in proxmox
  # ${count.index + 1}
  # this now reaches out to the vars file. I could've also used this var above in the pm_api_url setting but wanted to spell it out up there. target_node is different than api_url. target_node is which node hosts the template and thus also which node will host the new VM. it can be different than the host you use to communicate with the API. the variable contains the contents "prox-1u"
  target_node = var.proxmox_host
  # another variable with contents "ubuntu-2004-cloudinit-template"
  clone = var.template_name
  # basic VM settings here. agent refers to guest agent
  agent = 1
  os_type = "cloud-init"
  cores = 2
  sockets = 1
  cpu = "host"
  memory = 2200
  scsihw = "virtio-scsi-single"
  bootdisk = "scsi0"
  disk {
    slot = 0
    # set disk size here. leave it small for testing because expanding the disk takes time.
    size = "15G"
    type = "scsi"
    storage = "local-lvm"
    iothread = 1
  }
  
  # if you want two NICs, just copy this whole network section and duplicate it
  network {
    model = "virtio"
    bridge = "vmbr0"
  }
  # not sure exactly what this is for. presumably something about MAC addresses and ignore network changes during the life of the VM
  lifecycle {
    ignore_changes = [
      network,
    ]
  }
  
  # the ${count.index + 1} thing appends text to the end of the ip address
  ipconfig0 = "ip=10.1.0.10${count.index + 1}/24,gw=10.1.0.1"
  
  # sshkeys set using variables. the variable contains the text of the key.
  sshkeys = var.ssh_key
}
