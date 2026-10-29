#version 330
in vec2 local;
in vec4 tint;
in float selected;
uniform bool soft_style;
out vec4 output_color;
void main() {
    float r=length(local);
    float aa=max(fwidth(r),0.025);
    float body=1.0-smoothstep(1.0-aa,1.0+aa,r);
    float glow=soft_style ? exp(-5.0*max(r-0.7,0.0))*0.22 : 0.0;
    float light=soft_style ? 0.72+0.28*sqrt(max(0.0,1.0-dot(local,local)))+0.10*(-local.x+local.y) : 1.0;
    vec3 rgb=tint.rgb*light;
    float rim=selected*smoothstep(0.72,0.90,r)*(1.0-smoothstep(1.05,1.20,r));
    rgb=mix(rgb,vec3(1.0,0.86,0.48),rim);
    float a=max(max(body,glow),rim)*tint.a;
    if(a<0.002)discard;
    output_color=vec4(rgb,a);
}
