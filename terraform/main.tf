terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

#VOLUMES

resource "docker_volume" "postgre_data" {
  name = "ny_taxi_postgres_data"
}

resource "docker_volume" "pgadmin_data"{
  name = "pgadmin_data"
}

#NETWORK

resource "docker_network" "app_network" {
  name = "app_network"
}

#DATABASE POSTGRES
resource "docker_container" "pgdatabase"{
  name = "pgdatabase"
  image = "postgres:18"
  env = [
    "POSTGRES_USER=root",
    "POSTGRES_PASSWORD=root",
    "POSTGRES_DB=ny_taxi"
  ]

  ports {
    internal = 5432
    external = 5432
  }

  volumes {
    volume_name = docker_volume.postgre_data.name
    container_path = "/var/lib/postgresql"
  }

  networks_advanced {
    name = docker_network.app_network.name
  }
}

#PGADMIN
resource "docker_container" "pgadmin" {
  name  = "pgadmin"
  image = "dpage/pgadmin4"

  env = [
    "PGADMIN_DEFAULT_EMAIL=admin@admin.com",
    "PGADMIN_DEFAULT_PASSWORD=root",
    "PGADMIN_CONFIG_ENHANCED_COOKIE_PROTECTION=False",
    "PGADMIN_CONFIG_WTF_CSRF_ENABLED=False"
  ]

  ports {
    internal = 80
    external = 8085
  }

  volumes {
    volume_name = docker_volume.pgadmin_data.name
    container_path = "/var/lib/pgadmin"
  }

  networks_advanced {
    name = docker_network.app_network.name
  }
}

#TAXI_INGESTION
resource "docker_container" "taxi_ingest" {
  name  = "taxi_ingest"
  image = "taxi_ingest:v001"

  command = [
    "--pg-user=root",
    "--pg-pass=root",
    "--pg-host=pgdatabase",
    "--pg-port=5432",
    "--pg-db=ny_taxi",
    "--target-table=yellow_taxi_trips"
  ]

  networks_advanced {
    name = docker_network.app_network.name
  }

  depends_on = [
    docker_container.pgdatabase
  ]
}