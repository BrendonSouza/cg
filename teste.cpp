// Created by Darko (omegasbk) 
//
// Darko's Gamedev Cookbok Youtube serial
// https://www.youtube.com/channel/DarkoSupe
//
// Lesson 6 & 7 

struct Material 
{
    float diffuse;
    float specular;
    float shininess;
    float ambience;
    float reflection;
} materials[2];

struct Sphere 
{
    vec3 position;
    vec3 color;
    float radius;
    Material material;
} spheres[2];    
    
# define PLANES_COUNT 6
struct Plane 
{
    vec3 position;
    vec3 normal;
    vec3 color;
    Material material;
} planes[PLANES_COUNT];

struct Camera
{
    vec3 position;
    float focalDistance;
};
    
struct PointLight
{
    vec3 position;
    vec3 color;
    float intensity;
} lights[1];

const Material material1 = Material(0.514, 0.49, 76.8, 0.7, 1.);
const Material material2 = Material(0.4, 0.25, 124.3, 0.2, 1.);


Sphere sphere1 = Sphere(
    vec3(0.12, 0., 0.),  					// position
    vec3(0.1, 0.1, 0.3), 					// color
    0.08,									// radius
    material1);  // material

Sphere sphere2 = Sphere(
    vec3(-0.12, -0.05, 0.),  				// position
    vec3(0.3, 0.1, 0.1), 					// color
    0.08,									// radius
    material1);  // material

Plane plane1 = Plane(
    vec3(0., -0.2, 0.), 
    vec3(0., 1., 0.), 
    vec3(0.5, 0.5, 0.5), 
    material2);

Plane plane2 = Plane(
    vec3(-0.3, 0., 0.), 
    vec3(1., 0., 0.), 
    vec3(0.2, 0.5, 0.6), 
    material2);

Plane plane3 = Plane(
    vec3(0.3, 0., 0.), 
    vec3(-1., 0., 0.), 
    vec3(0.2, 0.5, 0.6), 
    material2);

Plane plane4 = Plane(
    vec3(0., 0.3, 0.), 
    vec3(0., -1., 0.), 
    vec3(0.2, 0.5, 0.6), 
    material2);

Plane plane5 = Plane(
    vec3(0., 0., .12), 
    vec3(0., 0., -1.), 
    vec3(0.2, 0.5, 0.6), 
    material2);

Plane plane6 = Plane(
    vec3(0., 0., -1.), 
    vec3(0., 0., 1.), 
    vec3(0.2, 0.5, 0.6), 
    material2);

PointLight light1 = PointLight(
    vec3(0., 0.19, -0.2), // position
    vec3(1., 1., 1.),     // color
    15.);                 // intensity

Camera camera = Camera(
    vec3(0., 0., -0.3),
    0.6);

#define SPHERE 0
#define PLANE 1

void setupScene()
{
	spheres[0] = sphere1;
    spheres[1] = sphere2;
    planes[0] = plane1;
    planes[1] = plane2;
	planes[2] = plane3;
    planes[3] = plane4;
	planes[4] = plane5;
    planes[5] = plane6;
    lights[0] = light1;
}

//////////////////////////////////////////////////////////////
// 	                        UTILS                           // 
//////////////////////////////////////////////////////////////
bool solveQuadratic(float a, float b, float c, out float t0, out float t1)
{
    float disc = b * b - 4. * a * c;
    
    if (disc < 0.)
    {
        return false;
    } 
    
    if (disc == 0.)
    {
        t0 = t1 = -b / (2. * a);
        return true;
    }
    
    t0 = (-b + sqrt(disc)) / (2. * a);
    t1 = (-b - sqrt(disc)) / (2. * a);
    return true;    
}

//////////////////////////////////////////////////////////////
// 	                   INTERSECTION CODE                    // 
//////////////////////////////////////////////////////////////
bool intersectSphere(
    vec3 origin, 
    vec3 direction, 
    Sphere sphere, 
    out float dist, 
    out vec3 surfaceNormal, 
    out vec3 Phit)
{
    vec3 L = origin - sphere.position;
    
    float a = dot(direction, direction);
    float b = 2. * dot(direction, L);
    float c = dot(L, L) - pow(sphere.radius, 2.);
    
    float t0;
    float t1;
    
    if (solveQuadratic(a, b, c, t0, t1))
    {        
        if (t0 > t1) 
        {
        	float temp = t0;
            t0 = t1;
            t1 = temp;
        } 
 
        if (t0 < 0.)
        { 
            t0 = t1; // if t0 is negative, let's use t1 instead 
            if (t0 < 0.) return false; // both t0 and t1 are negative 
        }  
             
        dist = t0;
       
        Phit = origin + dist * direction;
        surfaceNormal = normalize(Phit - sphere.position);               
        
        return true;
    }  
     
    return false;
}

bool intersectPlane(in Plane plane, in vec3 origin, in vec3 rayDirection, out float hitDistance) 
{ 
    // Assuming vectors are all normalized
    float denom = dot(plane.normal, rayDirection); 
    if (denom < 1e-6) 
    { 
        vec3 p0l0 = plane.position - origin; 
        hitDistance = dot(p0l0, plane.normal) / denom; 
        return (hitDistance >= 0.); 
    } 
 
    return false; 
} 

//////////////////////////////////////////////////////////////
// 	                     LIGTHING CODE                      // 
//////////////////////////////////////////////////////////////
void fresnel(vec3 I, vec3 N, float ior, out float kr) 
{ 
    float cosi = clamp(-1., 1., dot(I, N)); 
    
    float etai = 1., etat = ior; 
    
    if (cosi > 0.) 
    {
        float temp = etai;
        etai = etat;
        etat = temp;        
    } 
    
    // Compute sini using Snell's law
    float sint = etai / etat * sqrt(max(0., 1. - cosi * cosi)); 
    
    // Total internal reflection
    if (sint >= 1.)
    { 
        kr = 1.; 
    } 
    else 
    { 
        float cost = sqrt(max(0., 1. - sint * sint)); 
        cosi = abs(cosi); 
        float Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost)); 
        float Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost)); 
        kr = (Rs * Rs + Rp * Rp) / 2.; 
    } 
    // As a consequence of the conservation of energy, transmittance is given by:
    // kt = 1 - kr;
} 

void calculateShadow(vec3 pHit, inout vec3 finalColor, in float ambient, int type, int index)
{
    // Intersect spheres
    vec3 shadowSurfaceNormal;
    vec3 shadowRay = lights[0].position - pHit;
    vec3 shadowRayDirection = normalize(shadowRay);
    float distanceToLight = sqrt(dot(shadowRay, shadowRay));
    vec3 shadowPhit;
    
    float dist; 
    
    for(int i = 0; i < 2; ++i)
	{
        if (type == SPHERE && index == i)
        {
            continue;  
        }
    
        if (intersectSphere(pHit, shadowRay, spheres[i], dist, shadowSurfaceNormal, shadowPhit))
        {
            if (dist > 0. && distanceToLight > dist)
            {
            	finalColor *= 2. * ambient; // Educated guess
            }
        }
    }
    
    // Intersect planes
    for(int i = 0; i < PLANES_COUNT; ++i)
	{
 		if (type == PLANE && index == i)
        {
            continue;
        }
        
        if (intersectPlane(planes[i], pHit, shadowRay, dist))
        {    
            if (dist < distanceToLight)
            {                
 				finalColor *= 2. * ambient;        
            }
        }
    }     
}

vec3 getLitColor(in vec3 viewDir, in vec3 surfacePointPosition, in vec3 objectColor, in PointLight pointLight, in vec3 surfaceNormal, in Material material)
{
    vec3 lightVector = surfacePointPosition - pointLight.position;
    vec3 lightDir = normalize(lightVector);   
    
   	float lightIntensity = (pow(0.1, 2.) / pow(sqrt(dot(lightVector, lightVector)), 2.)) * pointLight.intensity;
    
    float coeff = -dot(lightDir, surfaceNormal);     
    
    vec3 ambient = material.ambience * objectColor;
        
    vec3 diffuse = material.diffuse * max(coeff, 0.) * objectColor * lightIntensity;
       
    vec3 halfwayDir = normalize(lightDir + viewDir);  
    vec3 specular = pow(max(-dot(surfaceNormal, halfwayDir), 0.0), material.shininess) * material.specular * objectColor * lightIntensity;
    
    vec3 color = ambient + diffuse + specular;
    
    return color;
}

Material getMaterial(int type, int index)
{
    if (type == SPHERE)
    {
        return spheres[index].material;
    }
    
    if (type == PLANE)
    {
        return planes[index].material;
    }
}

//////////////////////////////////////////////////////////////
// 	                       MAIN CODE                        // 
//////////////////////////////////////////////////////////////
vec3 rayMarch(in vec3 rayDirection, in vec3 rayOrigin)
{
    // Final color output - will be blended with all results below
    vec3 finalColor = vec3(0.);
    
    int BOUNCES = 2;
    
    int type = -1;
    int index = -1;
    
    int prevType = -1;
    int prevIndex = -1;
    
    for (int bounce = 0; bounce < BOUNCES; bounce++)
    {
        float dist =  1.0 / 0.0; // Infinity
        float planeHitDistance = dist;
        float sphereHitDistance = dist;

        vec3 passColor = vec3(0.);
    	vec3 surfaceNormal;
    	vec3 pHit;
        
        // Get color base
        // Intersect spheres
        for(int i = 0; i < 2; ++i)
        {
            if (prevType == SPHERE && prevIndex == i)
            {
                continue;
            }
            
            if (intersectSphere(rayOrigin, rayDirection, spheres[i], sphereHitDistance, surfaceNormal, pHit))
            {
                if (sphereHitDistance <= dist)
                {  
                    passColor = getLitColor(rayDirection, pHit, spheres[i].color, lights[0] /* TODO: support more lights */, surfaceNormal, spheres[i].material);        
                    calculateShadow(pHit, passColor, spheres[i].material.ambience, SPHERE, i);
                  
                    type = SPHERE;
                    index = i;
                    
                    dist = sphereHitDistance;
                }
            }
        }

        // Intersect planes
        for(int i = 0; i < PLANES_COUNT; ++i)
        {
            if (prevType == PLANE && prevIndex == i)
            {
                continue;
            }
            
            if (intersectPlane(planes[i], rayOrigin, rayDirection, planeHitDistance))
            {
                if (planeHitDistance <= dist)
                {    
                    passColor = getLitColor(rayDirection, rayOrigin + planeHitDistance * rayDirection, planes[i].color, lights[0] /* TODO: support more lights */, planes[i].normal, planes[i].material);        
                    dist = planeHitDistance;

                    pHit = rayOrigin + rayDirection * dist;
                    surfaceNormal = planes[i].normal;

                    calculateShadow(pHit, passColor, planes[i].material.ambience, PLANE, i);
                
                	type = PLANE;
                    index = i;
                }
            }
        } 
        
        if (bounce == 0)
        {
       		finalColor += passColor;
        }
        else
        {
            finalColor += getMaterial(prevType, prevIndex).specular * passColor;
        }
        
        rayOrigin = pHit;
        rayDirection = normalize(reflect(rayDirection, surfaceNormal));
        prevType = type;
        prevIndex = index;
    }
        
	return finalColor;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    setupScene();
    
    //camera.position.z += iMouse.y / iResolution.y / 4.;
    lights[0].position.x = (iMouse.x/ iResolution.x - 0.5) / 4.;
    lights[0].position.z = (iMouse.y/ iResolution.y - 0.5) / 3. - 0.3;
    
    // Normalized pixel coordinates (from -0.5 to 0.5)
    vec2 uv = fragCoord/iResolution.xy - 0.5;
    uv.x *= (iResolution.x / iResolution.y); 
    
    vec3 clipPlanePosition = vec3(uv.x, uv.y, camera.position.z + camera.focalDistance);
    vec3 rayDirection = normalize(clipPlanePosition - camera.position);
    
    vec3 finalColor = rayMarch(rayDirection, camera.position);
    
    // Fake antialiasing
    /*int sampleSize = 2;
    for (int i = -sampleSize; i < sampleSize; i++)
    {
        for (int j = -sampleSize; j < sampleSize; j++)
        {
            clipPlanePosition = vec3(uv.x + float(i) / iResolution.x, uv.y + float(j) / iResolution.y, camera.position.z + camera.focalDistance);
    		rayDirection = normalize(clipPlanePosition - camera.position);
            finalColor += rayMarch(rayDirection, camera.position);
        }
    }   
    finalColor /= pow(float(sampleSize) * 2., 2.);*/
    
    // Output to screen
    fragColor = vec4(finalColor, 1.0);
}