# Install Apache2 (assuming ApacheBench is included with Apache2-utils)
package { 'apache2':
  ensure => installed,
}

# Ensure Apache2 service is running
service { 'apache2':
  ensure => running,
}

# Configure Apache2 virtual host to listen on port 80
file { '/etc/apache2/sites-available/000-default.conf':
  ensure  => file,
  content => "Listen 80\n",
  notify  => Service['apache2'],
}

# Increase MaxClients in Apache2 configuration
file { '/etc/apache2/mods-available/mpm_prefork.conf':
  ensure  => file,
  content => "StartServers          5\nMinSpareServers       5\nMaxSpareServers      10\nMaxRequestWorkers    150\nMaxConnectionsPerChild 0\n",
  notify  => Service['apache2'],
}

# Increase worker_connections in Nginx configuration
file { '/etc/nginx/nginx.conf':
  ensure  => file,
  content => "worker_connections  1024;\n",
  notify  => Service['nginx'],
}

# Reload Apache2 and Nginx after configuration changes
exec { 'reload_apache2_nginx':
  command => 'service apache2 reload && service nginx reload',
  path    => '/usr/bin',
  require => [File['/etc/apache2/sites-available/000-default.conf'], File['/etc/apache2/mods-available/mpm_prefork.conf'], File['/etc/nginx/nginx.conf']],
}

# Disable default Apache2 site
file { '/etc/apache2/sites-enabled/000-default.conf':
  ensure => link,
  target => '/etc/apache2/sites-available/000-default.conf',
  notify => Service['apache2'],
}

# Ensure the required ApacheBench package is installed
package { 'apache2-utils':
  ensure => installed,
}
