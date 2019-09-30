variable "do_token" {}

terraform {
  required_version = "> 0.12.0"
}

locals {
  ssh_user = "yangliu"
  ssh_port = 20002
}

provider "digitalocean" {
  token = var.do_token
}

data "digitalocean_ssh_key" "ssh_key" {
  name = local.ssh_user
}

resource "digitalocean_droplet" "foo" {
  name = "foo"
  size = "s-1vcpu-1gb"
  image  = "49194090"
  region = "sgp1"
  ssh_keys = [data.digitalocean_ssh_key.ssh_key.id]
  user_data = templatefile(
    "${path.module}/cloud-config.yml",
    {
      ssh_user = local.ssh_user,
      ssh_port = local.ssh_port
      ssh_pub_key = file(pathexpand("~/.ssh/id_rsa.pub"))
    }
  )
}

resource "digitalocean_firewall" "fw" {
  name = "allow-ssh-from-office"

  droplet_ids = [digitalocean_droplet.foo.id]

  inbound_rule {
      protocol           = "tcp"
      port_range         = tostring(local.ssh_port)
      source_addresses   = ["114.242.94.82/32"]
  }

  outbound_rule {
      protocol                = "tcp"
      port_range              = "53"
      destination_addresses   = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
      protocol                = "udp"
      port_range              = "53"
      destination_addresses   = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
      protocol                = "icmp"
      destination_addresses   = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
      protocol                = "tcp"
      port_range              = "80"
      destination_addresses   = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
      protocol                = "tcp"
      port_range              = "443"
      destination_addresses   = ["0.0.0.0/0", "::/0"]
  }
}

resource "digitalocean_floating_ip" "ip" {
  droplet_id = digitalocean_droplet.foo.id
  region     = digitalocean_droplet.foo.region
}
