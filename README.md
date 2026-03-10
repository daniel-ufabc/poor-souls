# Local Development Setup (Ubuntu)

## Install dependencies

```bash
# Install Ruby and build dependencies
sudo apt update
sudo apt install -y ruby-full build-essential zlib1g-dev

# Configure gem installation to user directory
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Install Bundler
gem install bundler

# Install project dependencies
bundle install
```

## Run the server

```bash
bundle exec jekyll serve
```

For live reload during development:

```bash
bundle exec jekyll serve --livereload
```
