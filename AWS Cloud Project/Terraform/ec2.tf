# 9. Security Group for Bastion host (allow SSH from your IP)
resource "aws_security_group" "bastion_sg" {
  name        = "bastion_sg"
  description = "Allow SSH access"
  vpc_id      = aws_vpc.main-vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["165.91.13.238/32"] 
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}

# 10. Bastion Host in Public Subnet
resource "aws_instance" "bastion" {
  ami           = "ami-0cfde0ea8edd312d4"      
  instance_type = "t2.small"
  subnet_id     = aws_subnet.public.id
  key_name      = "ubuntu"                   
  security_groups = [aws_security_group.bastion_sg.id]

  tags = { Name = "bastion-host" }
}

# 11. Security Group for Private EC2s (allow SSH *from* Bastion)
resource "aws_security_group" "private_sg" {
  name        = "private_sg"
  vpc_id      = aws_vpc.main-vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    security_groups = [aws_security_group.bastion_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 12. Two EC2s in Private Subnet
resource "aws_instance" "private1" {
  ami               = "ami-0cfde0ea8edd312d4"  # Replace with a suitable AMI
  instance_type     = "t2.small"
  subnet_id         = aws_subnet.private.id
  key_name          = "ubuntu"               # Use same key for SSH
  security_groups   = [aws_security_group.private_sg.id]
  tags = { Name = "private-server-1" }
}

resource "aws_instance" "private2" {
  ami               = "ami-0cfde0ea8edd312d4"  # Replace with a suitable AMI
  instance_type     = "t2.small"
  subnet_id         = aws_subnet.private.id
  key_name          = "ubuntu"
  security_groups   = [aws_security_group.private_sg.id]
  tags = { Name = "private-server-2" }
}

resource "aws_security_group" "windows_sg" {
  name        = "windows_sg"
  vpc_id      = aws_vpc.main-vpc.id
  description = "Allow RDP access from bastion"

  ingress {
    from_port       = 3389
    to_port         = 3389
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion_sg.id] # RDP only from Bastion host
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 16. Windows Domain Controller in windows subnet
resource "aws_instance" "domain_controller" {
  ami               = "ami-0030d2097a16d86a8" # Windows Server 2019 DC, update as needed!
  instance_type     = "t3.medium"
  subnet_id         = aws_subnet.windows.id
  key_name          = "windows" 
  security_groups   = [aws_security_group.windows_sg.id]
  tags = { Name = "windows-domain-controller" }
  # user_data can be used to bootstrap DC setup (see Notes)
}

# 17. Windows client in windows subnet
resource "aws_instance" "windows_client" {
  ami               = "ami-0030d2097a16d86a8" # Use Windows Server or another Win AMI as desired
  instance_type     = "t3.medium"
  subnet_id         = aws_subnet.windows.id
  key_name          = "windows"
  security_groups   = [aws_security_group.windows_sg.id]
  tags = { Name = "windows-client" }
}

output "bastion_public_ip" {
  description = "Public IP of Bastion Host"
  value       = aws_instance.bastion.public_ip
}

output "private_server_1_private_ip" {
  description = "Private IP of Private Server 1"
  value       = aws_instance.private1.private_ip
}

output "private_server_2_private_ip" {
  description = "Private IP of Private Server 2"
  value       = aws_instance.private2.private_ip
}

output "windows_domain_controller_private_ip" {
  description = "Private IP of Windows Domain Controller"
  value       = aws_instance.domain_controller.private_ip
}

output "windows_client_private_ip" {
  description = "Private IP of Windows Client"
  value       = aws_instance.windows_client.private_ip
}