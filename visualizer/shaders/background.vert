#version 330
in vec2 corner;
out vec2 position;
void main() {gl_Position=vec4(corner,0.0,1.0);position=corner;}
